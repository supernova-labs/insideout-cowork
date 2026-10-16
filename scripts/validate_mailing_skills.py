"""Validate the Mailing distribution graph without touching operational data."""
import json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
P=ROOT/"plugins"/"insideout-mailing"
def validate():
 errors=[]
 schema=json.loads((P/"references/_shared/workbook-schema.json").read_text(encoding="utf-8"))
 expected={"gerir-contatos","montar-listas","gerir-historico"}
 paths=list((P/"skills").glob("*/SKILL.md"))
 if {p.parent.name for p in paths}!=expected:errors.append("Expected exactly three permanent skills")
 if len(schema["sheets"])!=7:errors.append("Expected exactly seven sheets")
 for name,cols in schema["sheets"].items():
  if len(cols)!=len(set(cols)) or not all(cols):errors.append("Invalid headers: "+name)
 for field,opts in schema["selections"].items():
  sheet,col=field.split(".",1)
  if col not in schema["sheets"][sheet] or len(opts)!=len(set(opts)):errors.append("Invalid selection: "+field)
 for sheet,keys in schema["keys"].items():
  if not set(keys)<=set(schema["sheets"][sheet]):errors.append("Invalid key: "+sheet)
 for source,field,target,key in schema["references"]:
  if field not in schema["sheets"][source] or key not in schema["sheets"][target]:errors.append("Invalid relationship")
 for path in paths:
  text=path.read_text(encoding="utf-8")
  if not text.startswith("---\nname: "+path.parent.name+"\ndescription: "):errors.append("Invalid frontmatter: "+path.parent.name)
  if len(text.splitlines())>=500:errors.append("Oversized skill")
  if not (path.parent/"agents/openai.yaml").is_file():errors.append("Missing UI metadata")
  if len(list((path.parent/"evals").glob("*.md")))<4:errors.append("Missing behavioral scenarios")
  for ref in re.findall(r"`([^\n`]+\.(?:md|json))`",text):
   resolved=(path.parent/ref).resolve()
   if not resolved.is_relative_to(P.resolve()) or not resolved.is_file():errors.append("Broken reference: "+ref)
 for path in P.rglob("*"):
  if path.is_file() and path.suffix not in {".md",".json",".yaml"}:errors.append("Executable/operational asset inside package")
 manifest=json.loads((P/".codex-plugin/plugin.json").read_text(encoding="utf-8"))
 if manifest["name"]!=P.name or manifest["version"]!="0.1.0" or manifest["skills"]!="./skills/":errors.append("Invalid manifest")
 catalog=json.loads((ROOT/".agents/plugins/marketplace.json").read_text(encoding="utf-8"))
 entries=[p for p in catalog["plugins"] if p["name"]==P.name]
 if len(entries)!=1 or entries[0]["source"]["path"]!="./plugins/"+P.name:errors.append("Invalid marketplace entry")
 index=json.loads((ROOT/".agent-smith/index.json").read_text(encoding="utf-8"))
 cs=[c for c in index["components"] if c.get("plugin")==P.name]
 if {c["name"] for c in cs}!=expected:errors.append("Index mismatch")
 for c in cs:
  adapters=[a for a in index["adapters"] if a["componentId"]==c["id"]]
  if len(adapters)!=1 or adapters[0]["path"]!=c["canonicalPath"]:errors.append("Adapter mismatch")
 return errors
if __name__=="__main__":
 errors=validate();print(json.dumps({"ok":not errors,"errors":errors},ensure_ascii=False,indent=2));raise SystemExit(bool(errors))
