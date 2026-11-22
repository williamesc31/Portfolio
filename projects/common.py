"""Small shared output helpers for the portfolio analyses."""
import json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def output_dir(base):
    out=Path(base)/'outputs'; out.mkdir(exist_ok=True); return out

def write_results(base, result):
    target=output_dir(base)/'results.json'
    target.write_text(json.dumps(result,indent=2,allow_nan=False,default=str)+'\n')
    print(json.dumps(result,indent=2,allow_nan=False,default=str))

def chart(base, name, fig):
    fig.tight_layout()
    fig.savefig(output_dir(base)/name,dpi=140,bbox_inches='tight')
    plt.close(fig)

plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,
                     'axes.spines.top':False,'axes.spines.right':False,
                     'axes.prop_cycle':plt.cycler(color=['#254f62','#4b8b70','#c28854','#8b7099'])})
