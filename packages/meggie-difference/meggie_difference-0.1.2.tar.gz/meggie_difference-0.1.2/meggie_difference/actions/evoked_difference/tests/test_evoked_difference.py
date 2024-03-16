from meggie_difference.utilities.testing import BaseDifferenceTestAction
from meggie_difference.actions.evoked_difference import EvokedDifference
from meggie_difference.utilities.dialogs.differenceDialogMain import (
    DifferenceDialog,
)


class TestEvokedDifference(BaseDifferenceTestAction):

    def test_evoked_difference(self):

        data = {"outputs": {"evoked": ["Evoked"]}}

        self.run_action(
            action_name="evoked_difference",
            handler=EvokedDifference,
            data=data,
            patch_paths=["meggie_difference.actions.evoked_difference"],
        )
        dialog = self.find_dialog(DifferenceDialog)
        dialog.differences = [("epochs_1", "epochs_2")]
        dialog.accept()
