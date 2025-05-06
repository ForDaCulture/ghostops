import argparse
from ghostrecon.recon_orchestrator import orchestrate, batch_run

def main():
    parser = argparse.ArgumentParser(prog="ghostrecon", description="GhostOps Recon CLI")
    sub = parser.add_subparsers(dest="command")

    single = sub.add_parser("scan", help="Scan a single domain/IP")
    single.add_argument("target", help="Target domain or IP")

    batch = sub.add_parser("batch", help="Scan multiple targets from a file")
    batch.add_argument("file", help="Path to text file with one domain/IP per line")

    args = parser.parse_args()

    if args.command == "scan":
        report = orchestrate(args.target)
        output_file = f"batch_reports/report_{args.target.replace('.', '_')}.json"
        with open(output_file, "w") as f:
            import json
            json.dump(report, f, indent=2)
        print(f"[✓] Report saved: {output_file}")

    elif args.command == "batch":
        with open(args.file) as f:
            targets = [line.strip() for line in f if line.strip()]
        batch_run(targets)

if __name__ == "__main__":
    main()
