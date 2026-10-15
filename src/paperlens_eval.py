import json, re
from collections import Counter

KEYS = ["task", "method", "datasets", "metrics", "main_result", "contribution_type"]
TYPES = {"new_method", "benchmark_or_dataset", "analysis", "survey", "other"}

def parse(text):
    """Dict if text is valid JSON with the right schema, else None."""
    try:
        t = re.sub(r"^```(?:json)?|```$", "", text.strip(), flags=re.M).strip()
        d = json.loads(t)
    except Exception:
        return None
    if not isinstance(d, dict) or set(d) != set(KEYS): return None
    if not all(isinstance(d[k], str) for k in ["task", "method", "main_result", "contribution_type"]): return None
    if not all(isinstance(d[k], list) and all(isinstance(x, str) for x in d[k]) for k in ["datasets", "metrics"]): return None
    if d["contribution_type"] not in TYPES: return None
    return d

toks = lambda s: re.findall(r"[a-z0-9]+", s.lower())
compact = lambda s: re.sub(r"[^a-z0-9]", "", s.lower())
nums = lambda s: re.findall(r"\d+(?:\.\d+)?", s)

def f1_from_counters(p, g):
    if not p and not g: return 1.0
    overlap = sum((p & g).values())
    if overlap == 0: return 0.0
    pr, rc = overlap / sum(p.values()), overlap / sum(g.values())
    return 2 * pr * rc / (pr + rc)

def tok_f1(p, g): return f1_from_counters(Counter(toks(p)), Counter(toks(g)))
def set_f1(p, g): return f1_from_counters(Counter({compact(x) for x in p if compact(x)}),
                                          Counter({compact(x) for x in g if compact(x)}))
def num_f1(p, g): return f1_from_counters(Counter(nums(p)), Counter(nums(g)))

def evaluate(preds, gold_rows, subset="all"):
    """preds: {id: raw model text}. gold_rows: rows of final/test.jsonl. subset: 'all' or 'reviewed'."""
    rows = [r for r in gold_rows if subset == "all" or r.get("reviewed")]
    names = ["valid", "task_f1", "method_f1", "datasets_f1", "metrics_f1",
             "datasets_f1_nonempty", "metrics_f1_nonempty", "type_acc",
             "result_num_f1", "result_tok_f1"]
    acc = {k: [] for k in names}
    for r in rows:
        g = json.loads(r["messages"][-1]["content"])
        p = parse(preds.get(r["id"], ""))
        sc = lambda fn, *a: 0.0 if p is None else fn(*a)
        acc["valid"].append(p is not None)
        acc["task_f1"].append(sc(tok_f1, p["task"] if p else "", g["task"]))
        acc["method_f1"].append(sc(tok_f1, p["method"] if p else "", g["method"]))
        acc["type_acc"].append(float(p is not None and p["contribution_type"] == g["contribution_type"]))
        for k in ["datasets", "metrics"]:
            s = sc(set_f1, p[k] if p else [], g[k])
            acc[f"{k}_f1"].append(s)
            if g[k]: acc[f"{k}_f1_nonempty"].append(s)
        acc["result_tok_f1"].append(sc(tok_f1, p["main_result"] if p else "", g["main_result"]))
        if nums(g["main_result"]):
            acc["result_num_f1"].append(sc(num_f1, p["main_result"] if p else "", g["main_result"]))
    out = {k: round(sum(v) / max(1, len(v)), 3) for k, v in acc.items()}
    out["n"] = len(rows)
    return out
