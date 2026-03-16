from invoke import task

@task
def git(ctx, message=None):
    """Run the testing script."""
    ctx.run(f"git add .")
    if message is None:
        message = "update"
    ctx.run(f"git commit -m '{message}'")
    ctx.run(f"git push origin main")