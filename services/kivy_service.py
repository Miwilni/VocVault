import sys

from widgets.toast import show_toast

def get_widget_from_grid_layout(instance, col_num: int = 0):
    try:
        grid_layout = instance.parent
        total_children = len(grid_layout.children)
        if total_children == 0:
            raise ValueError("GridLayout has no children")

        # Find the index of the clicked widget (Kivy stores children in reverse order)
        button_index = total_children - 1 - grid_layout.children.index(instance)

        # Calculate row and column position
        row = button_index // grid_layout.cols
        column = button_index % grid_layout.cols

        # Calculate the index of the target widget (same row, but column = col_num)
        target_index = row * grid_layout.cols + col_num

        # Ensure the target column exists in this row
        if col_num >= grid_layout.cols:
            raise ValueError(f"Column {col_num} does not exist in GridLayout (cols={grid_layout.cols})")

        # Kivy's children are stored in reverse order, so adjust the index
        target_child = grid_layout.children[total_children - 1 - target_index]

        return target_child
    except ValueError as e:
        show_toast(f"Error: {str(e)}")
        sys.exit("Fehler: Widget not found")
