#!/usr/bin/env python3
"""
resume_audit.py — deterministic checks for a resume, optionally against a job description.

Usage:
    python resume_audit.py resume.(txt|md|docx|pdf|tex) [--jd job.txt] [--json] [--exec]

Checks (each maps to a finding in references/research.md):
  * word count vs. 475–600 target (TalentWorks; --exec widens to 500–1000)
  * metric density: bullets with a number / total bullets; distinct metrics (Cultivated Culture: 36% have zero, 26% have 5+)
  * fluff blacklist, weak openers, pronouns (51% of resumes have at least one)
  * contact completeness: email, phone, LinkedIn, GitHub (48% include LinkedIn; +71% callbacks with a full profile)
  * bullets over 30 words; bullets not starting with a verb-like token
  * JD keyword coverage split hard/soft, ranked missing terms (avg 43 keywords/JD; 51% matched, 60% hard, 28% soft)
  * label lines (Tech Stack:, Coursework:, Languages:) are kept out of the per-bullet checks

Stdlib only. .docx via python-docx if installed, else zip+xml fallback. .pdf via pdftotext if on PATH, else pypdf if installed.
.tex via a built-in stripper (Jake's Resume macros and plain item/section), no dependencies.
Prefer source input (.md, .docx, .tex) over a PDF: PDF extraction splits each bullet at its line
breaks, so words-per-bullet and numbers-per-bullet come out wrong. Use the PDF for a final
round-trip check that contact details and section headers survive extraction.
"""

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import zipfile
from collections import Counter

# ---------------------------------------------------------------- text loading

def load_text(path: str) -> str:
    ext = os.path.splitext(path)[1].lower()
    if ext in (".txt", ".md", ".markdown", ""):
        with open(path, encoding="utf-8", errors="replace") as f:
            return f.read()
    if ext == ".docx":
        try:
            import docx  # type: ignore
            d = docx.Document(path)
            parts = []
            for p in d.paragraphs:
                is_list = "list" in (p.style.name or "").lower() or p._p.pPr is not None and p._p.pPr.numPr is not None
                parts.append(("- " + p.text) if is_list and p.text.strip() else p.text)
            for t in d.tables:
                for row in t.rows:
                    parts.append(" | ".join(c.text for c in row.cells))
            return "\n".join(parts)
        except ImportError:
            with zipfile.ZipFile(path) as z:
                xml = z.read("word/document.xml").decode("utf-8", "replace")
            xml = re.sub(r"</w:p>", "\n", xml)
            return re.sub(r"<[^>]+>", "", xml)
    if ext == ".pdf":
        if shutil.which("pdftotext"):
            out = subprocess.run(["pdftotext", "-layout", path, "-"], capture_output=True, text=True)
            return out.stdout
        try:
            from pypdf import PdfReader  # type: ignore
            return "\n".join((p.extract_text() or "") for p in PdfReader(path).pages)
        except ImportError:
            sys.exit("PDF input needs `pdftotext` on PATH or `pip install pypdf`.")
    if ext == ".tex":
        with open(path, encoding="utf-8", errors="replace") as f:
            return tex_to_text(f.read())
    sys.exit(f"Unsupported file type: {ext}")

# ---------------------------------------------------------------- LaTeX loading

def _read_group(s: str, i: int):
    """s[i] is '{'. Return (content, index just past the matching '}')."""
    depth, j = 0, i
    while j < len(s):
        c = s[j]
        if c == "\\":
            j += 2
            continue
        if c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
            if depth == 0:
                return s[i + 1:j], j + 1
        j += 1
    raise ValueError(f"unbalanced braces at offset {i}")

def _read_groups(s: str, i: int, n: int):
    out = []
    for _ in range(n):
        while i < len(s) and s[i] in " \t\r\n":
            i += 1
        if i >= len(s) or s[i] != "{":
            raise ValueError(f"expected '{{' at offset {i}")
        g, i = _read_group(s, i)
        out.append(g)
    return out, i

_TEX_WRAP = re.compile(r"\\(?:textbf|textit|emph|underline|texttt|textsc|small|scshape|Huge|large|Large|url|hbox|vcenter|mbox)\{((?:[^{}]|\{[^{}]*\})*)\}")
_TEX_HREF = re.compile(r"\\href\{[^{}]*\}\{((?:[^{}]|\{[^{}]*\})*)\}")
_TEX_MACRO = re.compile(r"\\(section\*?|resumeSubheading|resumeSubSubheading|resumeProjectHeading|resumeSubItem|resumeItem)(?![A-Za-z])")
_TEX_ARGC = {"section": 1, "section*": 1, "resumeSubheading": 4, "resumeSubSubheading": 2,
             "resumeProjectHeading": 2, "resumeSubItem": 1, "resumeItem": 1}

def _detex(s: str) -> str:
    """Plain text from a LaTeX fragment. Good enough for a resume, not a TeX parser."""
    s = re.sub(r"(?<!\\)%.*", "", s)
    s = _TEX_HREF.sub(r"\1", s)
    prev = None
    while prev != s:
        prev = s
        s = _TEX_WRAP.sub(r"\1", s)
    s = re.sub(r"\\(?:vspace|hspace)\*?\{[^{}]*\}", "", s)
    s = re.sub(r"\\begin\{[^{}]*\}(?:\[[^\]]*\])?", "", s)
    s = re.sub(r"\\end\{[^{}]*\}", "", s)
    s = re.sub(r"\\item(?![A-Za-z])", "\n- ", s)
    for tex, txt in ((r"$|$", " | "), (r"$\sim$", "~"), (r"$\times$", "x"), (r"\&", "&"), (r"\%", "%"),
                     (r"\#", "#"), (r"\$", "$"), (r"\_", "_"), ("``", '"'), ("''", '"'), ("\\\\", "\n")):
        s = s.replace(tex, txt)
    s = re.sub(r"(?<!-)--(?!-)", "-", s)
    s = re.sub(r"\\[A-Za-z]+\*?", "", s)   # any macro still standing: \Huge, \scshape, list wrappers ...
    s = s.replace("{", "").replace("}", "")
    s = re.sub(r"[ \t]+", " ", s)
    s = re.sub(r" *\n *", "\n", s)
    s = re.sub(r"^-\n(?=\S)", "- ", s, flags=re.M)   # `\item{` followed by a newline: rejoin the dash to its text
    return s.strip()

def tex_to_text(src: str) -> str:
    """Flatten a LaTeX resume: one line per heading, one `- ` line per bullet.

    Knows the Jake's Resume macros (resumeSubheading, resumeProjectHeading, resumeItem, ...)
    and plain item/section, which covers most LaTeX resumes. Anything else is stripped to
    its text. Each bullet comes out whole, which is the point: a PDF extract breaks bullets
    at line ends and every per-bullet number goes wrong.
    """
    body = src.split(r"\begin{document}", 1)[-1].split(r"\end{document}", 1)[0]
    out, pos = [], 0
    for m in _TEX_MACRO.finditer(body):
        if m.start() < pos:
            continue
        between = _detex(body[pos:m.start()])
        if between:
            out.append(between)
        name = m.group(1)
        try:
            args, pos = _read_groups(body, m.end(), _TEX_ARGC[name])
        except ValueError:
            out.append(_detex(body[m.end():]))
            pos = len(body)
            break
        args = [re.sub(r"\s+", " ", _detex(a)) for a in args]
        if name.startswith("section"):
            out.append("\n" + args[0].upper())
        elif name == "resumeSubheading":
            out.append(f"{args[0]} | {args[1]}")
            out.append(f"{args[2]} | {args[3]}")
        elif name in ("resumeSubSubheading", "resumeProjectHeading"):
            out.append(f"{args[0]} | {args[1]}")
        else:  # resumeItem / resumeSubItem
            out.append("- " + args[0])
    tail = _detex(body[pos:])
    if tail:
        out.append(tail)
    return "\n".join(out) + "\n"

# ---------------------------------------------------------------- lexicons

FLUFF = [
    "results-driven", "results driven", "detail-oriented", "detail oriented", "self-starter",
    "self starter", "go-getter", "team player", "hard worker", "hard-working", "hardworking",
    "passionate", "highly motivated", "motivated", "dynamic", "proactive", "strategic thinker",
    "thought leader", "guru", "ninja", "rockstar", "rock star", "wizard", "synergy", "synergistic",
    "best-of-breed", "best of breed", "value-add", "value add", "go-to person", "think outside the box",
    "outside the box", "proven track record", "track record of success", "track record",
    "excellent communication skills", "strong communication skills", "strong work ethic",
    "fast learner", "quick learner", "hit the ground running", "wear many hats", "references available",
    "seeking a challenging", "objective:", "robust", "scalable", "cutting-edge", "cutting edge",
    "state-of-the-art", "state of the art", "innovative", "seamless", "seamlessly", "world-class",
    "world class", "best-in-class", "best in class", "impactful", "leverage", "leveraged", "leveraging",
    "various", "numerous", "several", "many",
]

WEAK_OPENERS = [
    "responsible for", "duties included", "helped", "assisted", "assisted with", "worked on",
    "participated in", "involved in", "tasked with", "was part of", "part of", "contributed to",
    "utilized", "experience with", "experience in", "familiar with", "exposure to", "knowledge of",
]

PRONOUNS = re.compile(r"\b(I|me|my|mine|we|our|ours|he|she|they|them|their)\b")

# Soft-skill vocabulary used to split JD keywords into hard vs soft buckets.
SOFT_SKILLS = {
    "communication", "communicate", "collaboration", "collaborate", "collaborative", "leadership",
    "lead", "mentor", "mentoring", "mentorship", "ownership", "own", "initiative", "problem-solving",
    "problem solving", "analytical", "attention to detail", "organized", "organization", "adaptable",
    "adaptability", "teamwork", "team", "cross-functional", "stakeholder", "stakeholders",
    "prioritize", "prioritization", "time management", "self-motivated", "curious", "curiosity",
    "empathy", "customer-focused", "customer obsession", "bias for action", "influence",
    "presentation", "writing", "written", "verbal", "negotiation", "coaching", "facilitation",
    "decision-making", "decision making", "judgment", "autonomy", "independent", "independently",
    "fast-paced", "ambiguity", "learn", "learning", "growth mindset", "accountability", "accountable",
}

SHORT_TECH = {"go", "ml", "ai", "qa", "ci", "cd", "ux", "ui", "db", "os", "vm", "c#", "c++", "r"}

STOPWORDS = set("""
a an the and or but if then else of to in on at for from by with without as is are was were be been
being this that these those it its into over under between through during before after above below
up down out off again further once here there when where why how all any both each few more most other
some such no nor not only own same so than too very can will just should now you your we our they their
them he she his her i me my us who whom which what about across per via etc including include includes
required requirements preferred qualifications responsibilities role job position company team work
working experience years year plus strong ability able must have has had do does did done also well
new using use used need needs needed within provide provides provided support supports supported
ensure ensures build builds building develop develops developing developed design designs designing
designed help helps helping maintain maintains maintaining maintained write writes writing written
looking join participate participating take thrive thrives ideal candidate candidates bonus nice day daily
world people opportunity opportunities love want get make like great good best high quality across environment
culture benefits salary equal employer junior senior engineers seeking seek hiring hire offer offers apply
applicant applicants degree bachelor bachelors related field fields equivalent minimum least excellent
successful success proven record knowledge understanding familiarity solid demonstrated background
""".split())

NUMBER_RE = re.compile(
    r"(\$\s?\d[\d,.]*\s?[kKmMbB]?|\d[\d,.]*\s?%|\d[\d,.]*\s?[xX]\b|\b\d[\d,.]*\s?(k|K|M|B|MM)\b|\b\d[\d,.]*\b)"
)
DATE_LIKE = re.compile(
    r"\b(19|20)\d{2}\b|\b(jan|feb|mar|apr|may|jun|jul|aug|sep|sept|oct|nov|dec)[a-z]*\.?\s+\d{4}",
    re.I,
)

# ---------------------------------------------------------------- parsing helpers

BULLET_PREFIX = re.compile(r"^\s*([-•*▪◦●·–—]|\d+[.)])\s+")

# A label line is a bullet like `Tech Stack: Rust, Swift` or `Coursework: ...`: a short non-verb
# label, a colon, then a list. Inventory, not an achievement, so it stays out of the per-bullet
# metric and verb checks (it still counts toward words and distinct metrics).
LABEL_LINE = re.compile(r"^[A-Za-z][A-Za-z0-9 /&+-]{0,30}:\s")

def split_bullets(text: str):
    """Return (achievement bullets, other lines, label lines)."""
    bullets, others, labels = [], [], []
    for raw in text.splitlines():
        line = raw.strip()
        if not line:
            continue
        if BULLET_PREFIX.match(raw):
            b = BULLET_PREFIX.sub("", raw).strip()
            if LABEL_LINE.match(b) and not looks_like_verb(first_token(b)):
                labels.append(b)
            else:
                bullets.append(b)
        else:
            others.append(line)
    # Fallback: resumes exported without bullet glyphs — treat long sentence-lines as bullets
    if len(bullets) < 3:
        for line in others:
            if len(line.split()) >= 8 and not DATE_LIKE.search(line[:40]):
                bullets.append(line)
    return bullets, others, labels

def has_metric(s: str) -> bool:
    s_wo_dates = DATE_LIKE.sub(" ", s)
    return bool(NUMBER_RE.search(s_wo_dates))

def distinct_metrics(text: str):
    body = DATE_LIKE.sub(" ", text)
    # exclude phone-number-ish and zip-ish strings
    body = re.sub(r"\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}", " ", body)
    found = [m.group(0).strip() for m in NUMBER_RE.finditer(body)]
    return sorted(set(f for f in found if len(f.replace(",", "").replace(".", "")) < 12))

def first_token(s: str) -> str:
    return re.sub(r"[^A-Za-z-]", "", s.split()[0]) if s.split() else ""

def looks_like_verb(tok: str) -> bool:
    if not tok:
        return False
    t = tok.lower()
    if t in {"the", "a", "an", "this", "that", "our", "my", "in", "on", "for", "with", "as"}:
        return False
    # past tense or common imperative/present verbs used on resumes
    if t.endswith("ed") or t in {
        "led", "built", "ran", "drove", "cut", "set", "wrote", "shipped", "grew", "won", "sold", "spent",
        "made", "took", "held", "kept", "found", "brought", "taught", "rebuilt", "split", "ship", "build",
        "lead", "own", "manage", "drive", "design", "develop", "maintain", "run", "write", "reduce", "increase",
        "improve", "automate", "migrate", "deploy", "architect", "mentor", "launch", "create", "implement",
        "coordinate", "optimize", "scale", "integrate", "deliver", "analyze", "diagnose", "profile", "benchmark",
        "co-founded", "cofounded", "stood", "oversaw", "drew", "began", "sped", "co-led",
    }:
        return True
    return False

# ---------------------------------------------------------------- JD keywords

TECH_TOKEN = re.compile(r"[A-Za-z][A-Za-z0-9+#.\-/]{1,}")

def jd_keywords(jd: str, top_n: int = 60):
    text = jd.lower()
    def toks(seg):
        t = [x.strip(".,;:()") for x in TECH_TOKEN.findall(seg)]
        return [x for x in t if x and x not in STOPWORDS and not x.isdigit() and (len(x) > 2 or x in SHORT_TECH)]
    tokens = toks(text)
    uni = Counter(tokens)
    # bigrams only within a segment so they don't bridge headings, sentences, or list items
    bigrams = Counter()
    for seg in re.split(r"[.\n—–:;|()\[\]•*]", text):
        st = toks(seg)
        bigrams.update(f"{a} {b}" for a, b in zip(st, st[1:]))
    # keep bigrams that recur or are known soft-skill phrases
    keep_bi = {k: v for k, v in bigrams.items() if v >= 2 or k in SOFT_SKILLS}
    cands = Counter()
    cands.update(uni)
    cands.update(keep_bi)
    # drop unigrams fully covered by a kept bigram of equal frequency (e.g., "management" inside "time management")
    for bi, v in keep_bi.items():
        for part in bi.split():
            if cands.get(part) == v:
                cands.pop(part, None)
    ranked = [k for k, _ in cands.most_common(top_n)]
    hard = [k for k in ranked if k not in SOFT_SKILLS]
    soft = [k for k in ranked if k in SOFT_SKILLS]
    return hard, soft, cands

def coverage(keywords, resume_text):
    r = resume_text.lower()
    present, missing = [], []
    for k in keywords:
        # allow simple pluralization (either direction) and hyphen/space variants
        base = k[:-1] if (k.endswith("s") and not k.endswith("ss") and len(k) > 3) else k
        pat = re.escape(base).replace(r"\-", "[- ]").replace(r"\ ", "[- ]")
        if re.search(rf"(?<![a-z0-9]){pat}(?:s|es|ing|ed)?(?![a-z0-9])", r):
            present.append(k)
        else:
            missing.append(k)
    pct = round(100 * len(present) / len(keywords)) if keywords else None
    return pct, present, missing

# ---------------------------------------------------------------- main audit

def audit(resume_text: str, jd_text: str | None, exec_mode: bool):
    bullets, others, labels = split_bullets(resume_text)
    wc = len([t for t in resume_text.split() if re.search(r"[A-Za-z0-9]", t)])
    lo, hi = (500, 1000) if exec_mode else (475, 600)

    metric_bullets = [b for b in bullets if has_metric(b)]
    metrics = distinct_metrics(resume_text)

    low = resume_text.lower()
    fluff_hits = []
    for term in FLUFF:
        for m in re.finditer(rf"(?<![a-z-]){re.escape(term)}(?![a-z-])", low):
            line = resume_text[: m.start()].count("\n") + 1
            fluff_hits.append({"term": term, "line": line})
    weak = []
    for b in bullets:
        bl = b.lower()
        for w in WEAK_OPENERS:
            if bl.startswith(w):
                weak.append({"opener": w, "bullet": b[:90]})
                break
    pronoun_hits = [{"pronoun": m.group(0), "line": resume_text[: m.start()].count("\n") + 1}
                    for m in PRONOUNS.finditer(resume_text)]
    long_bullets = [b[:110] for b in bullets if len(b.split()) > 30]
    non_verb = [b[:90] for b in bullets if not looks_like_verb(first_token(b))]

    contact = {
        "email": bool(re.search(r"[\w.+-]+@[\w-]+\.[\w.-]+", resume_text)),
        "phone": bool(re.search(r"(\+\d{1,3}[\s.-]?)?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}", resume_text)),
        "linkedin": "linkedin.com/in/" in low or "linkedin.com/" in low,
        "github_or_portfolio": bool(re.search(r"github\.com/|gitlab\.com/|portfolio|https?://[\w.-]+\.(dev|io|me|com)\b", low)),
    }

    red_flags = []
    if re.search(r"\b(date of birth|dob|marital status|nationality)\b", low):
        red_flags.append("Personal data field present (DOB/marital status/nationality) — remove for North American resumes.")
    if re.search(r"references available", low):
        red_flags.append('"References available upon request" — delete.')
    if re.search(r"\bobjective\b\s*:", low):
        red_flags.append("Objective line — replace with a specific summary or delete.")
    if re.search(r"\((expert|advanced|intermediate|beginner|proficient|basic)\)", low) or re.search(r"\b(expert|intermediate|beginner|proficient)\s*[:(]", low) or re.search(r"\d{1,3}\s?%\s*(python|java|sql|excel)", low):
        red_flags.append("Self-rated proficiency levels detected — remove ratings; list only interviewable skills.")
    if re.search(r"\b(fig\.|figure|image|photo)\b", low[:400]):
        red_flags.append("Possible photo/image near the top — remove for ATS parsing and NA norms.")

    result = {
        "word_count": wc,
        "word_target": [lo, hi],
        "word_count_ok": lo <= wc <= hi,
        "bullets_total": len(bullets),
        "label_lines_excluded": len(labels),
        "bullets_with_metric": len(metric_bullets),
        "metric_bullet_pct": round(100 * len(metric_bullets) / len(bullets)) if bullets else 0,
        "distinct_metrics": len(metrics),
        "distinct_metrics_sample": metrics[:12],
        "fluff_hits": fluff_hits,
        "weak_openers": weak,
        "pronoun_hits": pronoun_hits[:20],
        "pronoun_count": len(pronoun_hits),
        "long_bullets_over_30_words": long_bullets,
        "bullets_not_starting_with_verb": non_verb[:15],
        "contact": contact,
        "red_flags": red_flags,
    }

    if jd_text:
        hard, soft, _ = jd_keywords(jd_text)
        hp, hpres, hmiss = coverage(hard, resume_text)
        sp, spres, smiss = coverage(soft, resume_text)
        allk = hard + soft
        ap, _, _ = coverage(allk, resume_text)
        result["jd"] = {
            "keywords_found_in_jd": len(allk),
            "overall_coverage_pct": ap,
            "hard_skill_coverage_pct": hp,
            "soft_skill_coverage_pct": sp,
            "hard_present": hpres,
            "hard_missing_ranked": hmiss[:25],
            "soft_present": spres,
            "soft_missing_ranked": smiss[:15],
            "benchmarks": {"avg_candidate_overall": 51, "avg_candidate_hard": 60, "avg_candidate_soft": 28},
        }
    return result

# ---------------------------------------------------------------- report

def render(r: dict) -> str:
    L = []
    ok = lambda b: "OK " if b else "!! "
    L.append(f"{ok(r['word_count_ok'])}Word count: {r['word_count']} (target {r['word_target'][0]}–{r['word_target'][1]})")
    excl = f"; {r['label_lines_excluded']} label line(s) excluded" if r.get("label_lines_excluded") else ""
    L.append(f"{ok(r['metric_bullet_pct'] >= 70)}Bullets with a number: {r['bullets_with_metric']}/{r['bullets_total']} ({r['metric_bullet_pct']}%) — target ≥70%{excl}")
    L.append(f"{ok(r['distinct_metrics'] >= 5)}Distinct metrics: {r['distinct_metrics']} — target ≥5 (36% of resumes have 0; 26% have 5+)")
    L.append(f"{ok(not r['fluff_hits'])}Fluff/buzzword hits: {len(r['fluff_hits'])}" +
             (" — " + ", ".join(f"{h['term']} (L{h['line']})" for h in r['fluff_hits'][:10]) if r['fluff_hits'] else ""))
    L.append(f"{ok(not r['weak_openers'])}Weak bullet openers: {len(r['weak_openers'])}" +
             ("\n     " + "\n     ".join(f"[{w['opener']}] {w['bullet']}" for w in r['weak_openers'][:8]) if r['weak_openers'] else ""))
    L.append(f"{ok(r['pronoun_count'] == 0)}Pronouns: {r['pronoun_count']}")
    L.append(f"{ok(not r['long_bullets_over_30_words'])}Bullets over 30 words: {len(r['long_bullets_over_30_words'])}")
    if r["bullets_not_starting_with_verb"]:
        L.append(f"!! Bullets not opening with a verb: {len(r['bullets_not_starting_with_verb'])}")
        for b in r["bullets_not_starting_with_verb"][:6]:
            L.append(f"     - {b}")
    c = r["contact"]
    L.append(f"{ok(all(c.values()))}Contact: email={c['email']} phone={c['phone']} linkedin={c['linkedin']} github/portfolio={c['github_or_portfolio']}")
    for f in r["red_flags"]:
        L.append(f"!! {f}")
    if "jd" in r:
        j = r["jd"]
        L.append("")
        L.append(f"JD alignment ({j['keywords_found_in_jd']} keywords extracted; avg JD has ~43)")
        L.append(f"{ok((j['overall_coverage_pct'] or 0) >= 70)}Overall coverage: {j['overall_coverage_pct']}%  (avg candidate: 51%)")
        L.append(f"{ok((j['hard_skill_coverage_pct'] or 0) >= 75)}Hard-skill coverage: {j['hard_skill_coverage_pct']}%  (avg candidate: 60%)")
        L.append(f"{ok((j['soft_skill_coverage_pct'] or 0) >= 50)}Soft-skill coverage: {j['soft_skill_coverage_pct']}%  (avg candidate: 28%) — demonstrate inside bullets, don't list")
        if j["hard_missing_ranked"]:
            L.append("   Missing hard terms (by JD frequency): " + ", ".join(j["hard_missing_ranked"][:20]))
        if j["soft_missing_ranked"]:
            L.append("   Missing soft terms: " + ", ".join(j["soft_missing_ranked"][:10]))
        L.append("   Only add terms the candidate can truthfully claim. Keyword extraction is heuristic — sanity-check the list.")
    return "\n".join(L)

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("resume")
    ap.add_argument("--jd", help="job description file (txt/md)")
    ap.add_argument("--json", action="store_true", help="emit JSON instead of a text report")
    ap.add_argument("--exec", action="store_true", help="executive/CV mode: widen word target to 500–1000")
    a = ap.parse_args()
    resume_text = load_text(a.resume)
    jd_text = load_text(a.jd) if a.jd else None
    r = audit(resume_text, jd_text, a.exec)
    print(json.dumps(r, indent=2) if a.json else render(r))

if __name__ == "__main__":
    main()
