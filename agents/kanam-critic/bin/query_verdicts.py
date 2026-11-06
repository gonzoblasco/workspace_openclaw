#!/usr/bin/env python3
import sys, json, argparse, os

def main():
    parser = argparse.ArgumentParser(description='Query recorded SHARP verdicts')
    parser.add_argument('--artifact', help='Filter results by artifact identifier')
    parser.add_argument('--all', action='store_true', help='Show all verdicts (default)')
    args = parser.parse_args()
    # Path to JSONL file
    storage_path = os.path.join(os.path.dirname(__file__), '..', 'memory', 'verdicts.jsonl')
    if not os.path.exists(storage_path):
        print('No verdicts recorded yet.', file=sys.stderr)
        sys.exit(0)
    with open(storage_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    filtered = []
    for line in lines:
        try:
            rec = json.loads(line)
        except json.JSONDecodeError:
            continue
        if args.artifact:
            if rec.get('artifact') == args.artifact:
                filtered.append(rec)
        else:
            filtered.append(rec)
    if not filtered:
        print('No matching verdicts found.')
        return
    # Print in a readable table format
    # Header
    print(f"{'Artifact':<20} {'Verdict':<10} {'Total':<5} {'Timestamp':<25} {'Scores (S H A R P)':<15}")
    print('-' * 85)
    for rec in filtered:
        art = rec.get('artifact','')
        verdict = rec.get('verdict','')
        total = rec.get('total','')
        ts = rec.get('timestamp','')
        scores = rec.get('scores',{})
        scores_str = f"{scores.get('S','')}/{scores.get('H','')}/{scores.get('A','')}/{scores.get('R','')}/{scores.get('P','')}"
        # Un veredicto retirado se muestra como ANULADO, nunca como vigente: mostrar
        # 'Aprobado' de una fila invalidada es un verde falso (medido el 2026-11-06).
        if rec.get('status') == 'invalidated':
            verdict = 'ANULADO'
        print(f"{art:<20} {verdict:<10} {total:<5} {ts:<25} {scores_str:<15}")
        if rec.get('status') == 'invalidated':
            print(f"{'':<20} motivo: {rec.get('invalidation_reason', '(sin motivo escrito)')}")

if __name__ == '__main__':
    main()
