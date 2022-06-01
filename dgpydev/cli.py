import click


@click.group()
@click.option("--debug/--no-debug", default=False)
def cli(debug):
    click.echo(f"Debug mode is {'on' if debug else 'off'}")


@cli.command()
def update():
    click.echo("updating")
    raise NotImplementedError("TODO")


def main():
    cli()


if __name__ == "__main__":
    main()
