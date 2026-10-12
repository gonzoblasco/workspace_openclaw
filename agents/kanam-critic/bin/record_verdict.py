#!/usr/bin/env python3
import sys, json, os, datetime, argparse

def main():
    parser = argparse.ArgumentParser(description="Record a SHARP verdict")
    parser.add_argument('--artifact', required=True, help='Identifier of the evaluated artifact')
    parser.add_argument('--S', type=int, required=True, help='Score for Sharpness (1-5)')
    parser.add_argument('--H', type=int, required=True, help='Score for Horizon (1-5)')
    parser.add_argument('--A', type=int, required=True, help='Score for Asymmetry (1-5)')
    parser.add_argument('--R', type=int, required=True, help='Score for Resistance (1-5)')
    parser.add_argument('--P', type=int, required=True, help='Score for Parsimony (1-5)')
    parser.add_argument('--verdict', required=True, choices=['VETO','Aprobado','ORO'], help='Overall verdict')
    parser.add_argument('--notes', default='', help='Optional free‑form notes')
    args = parser.parse_args()
    # basic validation (scores between 1 and 5)
    for axis_name in ['S','H','A','R','P']:
        val = getattr(args, axis_name)
        if not (1 <= val <= 5):
            print(f"Error: {axis_name} must be between 1 and 5 (got {val})", file=sys.stderr)
            sys.exit(1)
    total = args.S + args.H + args.A + args.R + args.P
    timestamp = datetime.datetime.utcnow().isoformat() + 'Z'
    record = {
        "artifact": args.artifact,
        "scores": {"S": args.S, "H": args.H, "A": args.A, "R": args.R, "P": args.P},
        "total": total,
        "verdict": args.verdict,
        "notes": args.notes,
        "timestamp": timestamp
    }
    # Ensure memory directory exists
    storage_dir = os.path.join(os.path.dirname(__file__), '..', 'memory')
    os.makedirs(storage_dir, exist_ok=True)
    storage_path = os.path.join(storage_dir, 'verdicts.jsonl')
    with open(storage_path, 'a', encoding='utf-8') as f:
        json.dump(record, f)
        f.write('\n')
    print(f"Recorded verdict for {args.artifact} at {timestamp}")

if __name__ == '__main__':
    main()
