from datetime import datetime
from pathlib import Path
import sys
from wizlib.parser import WizParser
from wizlib.ui import Chooser
from wizlib.ui import Choice

from filez4eva.command import Filez4EvaCommand
from filez4eva.error import Filez4EvaError


class StowCommand(Filez4EvaCommand):
    """Move filez to the right place with the right name"""

    name = 'stow'

    date: str
    account: str
    part: str

    @classmethod
    def add_args(cls, parser: WizParser):
        super().add_args(parser)
        parser.add_argument('--date', '-d')
        parser.add_argument('--account', '-a')
        parser.add_argument('--part', '-p')
        parser.add_argument('file')

    def handle_vals(self):
        super().handle_vals()
        if not self.provided('date'):
            while True:
                self.date = self.ui.get_text('Date: ')
                try:
                    datetime.strptime(self.date, "%Y%m%d")
                    break
                except ValueError:
                    print('Date must match format YYYYMMDD', file=sys.stderr)

    @Filez4EvaCommand.wrap
    def execute(self):
        targetdir = Path(self.config.get('filez4eva-target'))
        sourcepath = Path(self.file).expanduser().absolute()
        if not sourcepath.is_file():
            raise Filez4EvaError(f"Missing file {sourcepath}")
        extension = sourcepath.suffix
        date = datetime.strptime(self.date, "%Y%m%d")
        dirpath = targetdir / str(date.year) / self.account
        if not dirpath.exists():
            # confirm = rlinput(f"Create {dirpath}? ", default="yes")
            # if confirm.startswith('y'):
            dirpath.mkdir(parents=True)
        targetpath = dirpath / \
            f"{date.strftime('%Y%m%d')}-{self.part}{extension}"
        if targetpath.exists():
            raise Filez4EvaError(f"File already exists at {targetpath}")
        # confirm = rlinput(f"Move file to {targetpath}? ", default="yes")
        # if confirm.startswith('y'):
        sourcepath.rename(targetpath)
        self.status = 'Done'
