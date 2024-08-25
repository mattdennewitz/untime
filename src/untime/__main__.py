import json

import click

from .complexity import analyze_file


@click.group()
def cli(): ...


@cli.command('analyze')
@click.option(
    "-i",
    "--input-path",
    type=click.Path(exists=True, dir_okay=False, file_okay=True),
    help="Analyze a Python file for McCabe complexity.",
)
def run_analysis(input_path: str):
    """
    Analyzes a file, emits a report.

    Args:
        input_file: Path to file to scan
    """

    scores, total_score = analyze_file(input_path)

    digest = {rule: score for (rule, score) in scores.items()}

    click.echo(json.dumps(digest, indent=2))


if __name__ == "__main__":
    cli()
