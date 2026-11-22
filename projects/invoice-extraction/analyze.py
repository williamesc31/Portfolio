"""Extract a documented invoice text layout and validate its arithmetic exactly."""
from pathlib import Path
from decimal import Decimal,InvalidOperation
from datetime import date
import argparse,json,re
BASE=Path(__file__).resolve().parent

def extract(text):
    def field(name):
        values=re.findall(r'^'+re.escape(name)+r':\s*(.+)$',text,re.MULTILINE)
        if len(values)!=1:raise ValueError(f'Expected exactly one {name} field')
        return values[0].strip()
    def money(value):
        try:result=Decimal(value.replace('$','').replace(',','').strip())
        except InvalidOperation as exc:raise ValueError('Invalid currency amount') from exc
        if not result.is_finite() or result<0 or result!=result.quantize(Decimal('.01')):raise ValueError('Money must be nonnegative with at most two decimals')
        return result
    number=field('Invoice');vendor=field('Vendor');customer=field('Customer')
    issued=field('Date');date.fromisoformat(issued)
    items=[]
    for line in text.splitlines():
        if '|' not in line:continue
        parts=[x.strip() for x in line.split('|')]
        if parts==['Quantity','Description','Unit price']:continue
        if len(parts)!=3:raise ValueError('Malformed line item')
        quantity=money(parts[0]);price=money(parts[2])
        if quantity<=0 or not parts[1]:raise ValueError('Line item needs a positive quantity and description')
        total=(quantity*price).quantize(Decimal('.01'))
        items.append({'quantity':str(quantity),'description':parts[1],'unit_price':str(price.quantize(Decimal('.01'))),'line_total':str(total)})
    if not items:raise ValueError('No line items found')
    subtotal=money(field('Subtotal'));tax=money(field('Tax'));total=money(field('Total'))
    if sum(Decimal(x['line_total']) for x in items)!=subtotal:raise ValueError('Line items do not match subtotal')
    if subtotal+tax!=total:raise ValueError('Subtotal plus tax does not match total')
    return {'invoice_number':number,'vendor':vendor,'customer':customer,'date':issued,'currency':'USD','line_items':items,
            'subtotal':str(subtotal.quantize(Decimal('.01'))),'tax':str(tax.quantize(Decimal('.01'))),'total':str(total.quantize(Decimal('.01'))),'arithmetic_valid':True}

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--input',type=Path);args=parser.parse_args()
    out=BASE/'outputs';out.mkdir(exist_ok=True)
    if args.input:
        print(json.dumps(extract(args.input.read_text()),indent=2));return
    examples=[]
    for path in sorted((BASE/'data').glob('invoice_*.txt')):
        result=extract(path.read_text());examples.append(result)
    assert len(examples)==3
    try:extract((BASE/'data/invalid_total.txt').read_text())
    except ValueError:rejected=True
    else:raise AssertionError('Inconsistent invoice should have been rejected')
    (out/'extracted_invoices.json').write_text(json.dumps(examples,indent=2)+'\n')
    result={'valid_fixtures_processed':len(examples),'invalid_total_fixture_rejected':rejected,
        'invoice_numbers':[x['invoice_number'] for x in examples],
        'method':'Anchored field extraction, explicit line-item grammar, ISO date validation, exact Decimal arithmetic',
        'limits':'Fixtures are fictional regression examples, not a benchmark. This local parser supports the documented text layout; it does not perform OCR or call an LLM.'}
    (out/'results.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':main()
