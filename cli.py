"""Command-line interface for Summ-AI-rize.

Examples:
    python cli.py --url https://youtube.com/watch?v=VIDEO_ID
    python cli.py --file transcript.txt
    python cli.py --url ... --depth deep
    python cli.py --file transcript.txt --output summary.md
    python cli.py --url ... --depth concise --model llama3.2:1b
"""
import argparse
import sys
from summarizer import YouTubeSummarizer


def main():
    parser = argparse.ArgumentParser(
        description="Summ-AI-rize CLI: summarize YouTube videos or transcript files from the command line.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="Make sure Ollama is running and required models are pulled before use.",
    )

    src = parser.add_mutually_exclusive_group(required=True)
    src.add_argument("--url", help="YouTube URL to summarize")
    src.add_argument("--file", help="Path to a transcript text file")

    parser.add_argument(
        "--depth",
        choices=["concise", "standard", "deep"],
        default="standard",
        help="Summary depth (default: standard)",
    )
    parser.add_argument("--model", default="llama3.2", help="Ollama model name (default: llama3.2)")
    parser.add_argument("--output", help="Write summary to this file (default: stdout)")
    parser.add_argument("--quiet", action="store_true", help="Suppress progress messages")

    args = parser.parse_args()

    def log(msg):
        if not args.quiet:
            print(msg, file=sys.stderr)

    log(f"[CLI] Initializing summarizer (model={args.model}, depth={args.depth})")
    summarizer = YouTubeSummarizer(model=args.model, depth=args.depth)

    if args.url:
        log(f"[CLI] Summarizing URL: {args.url}")
        result = summarizer.summarize_video(args.url)
        if result["status"] != "success":
            print(f"Error: {result['message']}", file=sys.stderr)
            sys.exit(1)
    else:
        log(f"[CLI] Reading transcript from: {args.file}")
        try:
            with open(args.file, "r", encoding="utf-8") as f:
                transcript = f.read()
        except FileNotFoundError:
            print(f"Error: file not found: {args.file}", file=sys.stderr)
            sys.exit(1)
        result = summarizer.summarize_text(transcript)

    summary = result["summary"]

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(summary)
        log(f"[CLI] Summary written to: {args.output}")
    else:
        print(summary)

    log(
        f"[CLI] Done. type={result.get('type_label')} "
        f"words={result.get('summary_words')} "
        f"time={result.get('elapsed_seconds')}s"
    )


if __name__ == "__main__":
    main()
