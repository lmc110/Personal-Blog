import os, sys, re

# TODO Change this to import from your main application file
from main import app

import subprocess
from flask_script import Manager

manager = Manager(app)

_status_re = re.compile('^(.)(.) (.*)')

@manager.command
def package(output_file = 'submission.zip', force=False):
    """Prepares a package for assignment submission."""
    print('checking repository status')
    os.chdir(app.root_path)
    if os.path.exists('__init__.py'):
        print('found __init__.py, assuming in package')
        os.chdir('..')
    if not os.path.exists('manage.py'):
        print('manage.py not found, something is likely wrong',
              file=sys.stderr)
    if not os.path.exists('.git'):
        if not force:
            print("this doesn't look like a Git repository, bailing",
                  file=sys.stderr)
            print("use --force to override", file=sys.stderr)
            sys.exit(1)
        else:
            print("this doesn't look like a Git repository, continuing anyway",
                  file=sys.stderr)
    proc = subprocess.Popen(['git', 'status', '--porcelain'], stdout=subprocess.PIPE)
    with proc.stdout:
        bad = False
        for line in proc.stdout:
            match = _status_re.match(line.decode())
            if not match:
                continue
            file = match.group(3)
            x = match.group(1)
            y = match.group(2)
            if x+y == '??':
                print('untracked file {}, did you mean to add?'.format(file),
                      file=sys.stderr)
            else:
                print('uncommitted changes to {}'.format(file),
                      file=sys.stderr)
            bad = True
        if bad:
            if force:
                print('uncommitted changes (proceeding anyway)',
                      file=sys.stderr)
            else:
                print('uncommitted changes, cancelling (--force to proceed anyway)',
                      file=sys.stderr)
                sys.exit(2)

    app.logger.info('creating git archive')
    pfx, ext = os.path.splitext(os.path.basename(output_file))
    rc = subprocess.call(['git', 'archive', '--prefix={}/'.format(pfx),
                          '-o', output_file, 'HEAD'])
    if rc:
        print('git archive failed with code {}'.format(rc), file=sys.stderr)
        sys.exit(3)
    print('wrote archive to {}'.format(output_file))


if __name__ == '__main__':
    manager.run()
