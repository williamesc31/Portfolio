"""Run every showcased project and record reproducibility evidence."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,platform,subprocess,sys,time
ROOT=Path(__file__).resolve().parents[1]
PROJECTS=['credit-risk-prediction','bank-marketing-targeting','cfpb-complaint-forecasting',
          'childcare-affordability','netflix-engagement','tsa-complaints','movie-recommendations',
          'lottery-number-analysis','white-house-visits','invoice-extraction']

def main():
    records=[]
    for name in PROJECTS:
        command=['python',f'projects/{name}/analyze.py']
        started=time.perf_counter()
        result=subprocess.run([sys.executable,str(ROOT/command[1])],cwd=ROOT,text=True,capture_output=True)
        target=ROOT/'projects'/name/'outputs/results.json'
        if result.returncode or not target.is_file():
            print(result.stderr or result.stdout,file=sys.stderr)
            raise SystemExit(f'FAIL: {name}')
        parsed=json.loads(target.read_text(),parse_constant=lambda value:(_ for _ in ()).throw(ValueError(value)))
        if not isinstance(parsed,dict) or not parsed:raise SystemExit(f'Empty results: {name}')
        records.append({'project':name,'command':' '.join(command),'status':'passed',
            'seconds':round(time.perf_counter()-started,2),'results_sha256':hashlib.sha256(target.read_bytes()).hexdigest()})
        print(f'PASS {name}')
    inputs={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest()
            for p in sorted((ROOT/'projects').rglob('*')) if p.is_file() and (p.suffix=='.py' or 'data' in p.parts) and '__pycache__' not in p.parts}
    report={'verified_at_utc':datetime.now(timezone.utc).isoformat(),'python':platform.python_version(),
            'passed':len(records),'projects':records,'input_and_code_sha256':inputs,
            'scope':'All default analysis commands executed end to end against bundled snapshots. No paid API, GPU, or external service required.'}
    (ROOT/'VERIFICATION.json').write_text(json.dumps(report,indent=2)+'\n')
    print(f'All {len(records)} projects passed; see VERIFICATION.json')
if __name__=='__main__':main()
