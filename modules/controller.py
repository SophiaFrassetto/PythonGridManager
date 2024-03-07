import sys
from uuid import uuid4

from utils import bprint, clear_windown, resize_windown, DEFAULT_DECORATIONS, DEFAULT_COLORS, DEFAULT_BG_COLORS

__all__ = ['Grid']


class Grid:
    DEFAULT_SEP_H = '─'
    DEFAULT_SEP_V = '│'

    DEFAULT_SEP_TR = '┐'
    DEFAULT_SEP_TL = '┌'
    DEFAULT_SEP_BR = '┘'
    DEFAULT_SEP_BL = '└'

    DEFAULT_SEP_HR = '┤'
    DEFAULT_SEP_HL = '├'
    DEFAULT_SEP_VT = '┬'
    DEFAULT_SEP_VB = '┴'

    DEFAULT_SEP_I = '┼'
    GRID = {}

    def __init__(self, name, cell_size=35, columns=3, lines=50, default_text_color=None, default_bg_color=None, default_text_style=None, grid_color=None, grid_name_color=None):
        divisions = [1]
        divisions.extend([(i * (cell_size+2)) for i in range(1, columns)])
        
        cells = {
            f'{lpos}_{i+1}': {
                'line': lpos,
                'column': dpos+1,
                'last_column': dpos+cell_size-1,
                'value': None,
                'text_color': default_text_color,
                'bg_color': default_bg_color,
                'text_style': default_text_style,
            }
            for lpos in range(1, lines+1)
            for i, dpos in enumerate(divisions)
        }
        
        self.GRID = {
            'id': uuid4(),
            'name': name,
            'cells': cells,
            'cell_size': cell_size,
            'lines': lines,
            'columns': columns,
            'total_column_size': int((cell_size+2)*columns)-2,
            'divisions': divisions,
            'grid_color': grid_color,
            'grid_name_color': grid_name_color
        }

    def show_grid(self):
        # resize and clear terminal
        resize_windown(self.GRID['lines']+4, self.GRID['total_column_size']+3)
        clear_windown()
        
        grid_color = self.GRID['grid_color']
        grid_name_color = self.GRID['grid_name_color']

        show_params = []

        _show_params = lambda cm, l, clm, clr: {'command': cm, 'lines':l, 'columns':clm, 'color':clr, 'reset_cursor':True}
        
        def _set_margim_div(line, sep, grid_color):
            show_params = []
            for div in self.GRID['divisions']:
                if div == 1:
                    continue

                show_params.append(
                    _show_params(sep, line, div, grid_color)
                )
            return show_params

        # set top line
        top_line = self.DEFAULT_SEP_TL + self.DEFAULT_SEP_H*self.GRID['total_column_size'] + self.DEFAULT_SEP_TR
        show_params.append(
            _show_params(top_line, 2, 1, grid_color)
        )
        
        # set top line division edge
        show_params.extend(_set_margim_div(2, self.DEFAULT_SEP_VT, grid_color))

        # set top line name
        grid_name_position = self.GRID['name'].center(self.GRID['total_column_size'], self.DEFAULT_SEP_H).find(next(filter(str.isalpha, self.GRID['name'])))
        show_params.append(
            _show_params(self.GRID['name'], 2, grid_name_position+1, grid_name_color)
        )
        
        # set bottom line
        bottom_line = self.DEFAULT_SEP_BL + self.DEFAULT_SEP_H*self.GRID['total_column_size'] + self.DEFAULT_SEP_BR
        show_params.append(
            _show_params(bottom_line, self.GRID['lines']+3, 1, grid_color)
        )

        # set bottom line division edge
        show_params.extend(_set_margim_div(self.GRID['lines']+3, self.DEFAULT_SEP_VB, grid_color))

        # set lines and cells and cell value
        for _, cell in self.GRID['cells'].items():
            # set line and cell division
            show_params.append(
                _show_params(self.DEFAULT_SEP_V, cell['line']+2, cell['column']-1, grid_color)
            )
            # set last column
            show_params.append(
                _show_params(self.DEFAULT_SEP_V, cell['line']+2, self.GRID['total_column_size']+2, grid_color)
            )
            
            # set cell value
            if cell['value']:
                show_params.append(
                    {
                        'command': cell['value'][:self.GRID['cell_size']],
                        'lines': cell['line']+2,
                        'columns': cell['column'],
                        'color': cell['text_color'],
                        'bg_color': cell['bg_color'],
                        'decoration': cell['text_style'],
                        'reset_cursor':True,
                    }
                )
        
        # show grid
        for sp in show_params:
            bprint(**sp)
        
    def add_cell_value(self, line, column, value, text_color=None, bg_color=None, text_style=None):
        cell_id = f'{line}_{column}'
        
        if cell_id in self.GRID['cells']:
            self.GRID['cells'][cell_id]['value'] = value
        
        if text_color:
            self.GRID['cells'][cell_id]['text_color'] = text_color
        if bg_color:
            self.GRID['cells'][cell_id]['bg_color'] = bg_color
        if bg_color:
            self.GRID['cells'][cell_id]['text_style'] = text_style

        self.show_grid()

# g = Grid(
#     name='Estoca Front Robot', 
#     cell_size=35,
#     columns=4,
#     lines=50,
#     default_text_color=DEFAULT_COLORS.RED.value,
#     default_bg_color=DEFAULT_BG_COLORS.GREEN.value,
#     default_text_style=DEFAULT_DECORATIONS.BOLD.value,
#     grid_color=DEFAULT_COLORS.BLUE.value,
#     grid_name_color=DEFAULT_COLORS.RED.value
# )

# g.show_grid()

# g.add_cell_value(
#      line=1,
#      column=1,
#      value='TESTE',
#      text_color=DEFAULT_COLORS.GREEN.value,
#      bg_color=DEFAULT_BG_COLORS.WHITE.value,
#      text_style=DEFAULT_DECORATIONS.UNDERLINE.value
# )

# g.add_cell_value(
#      line=1,
#      column=2,
#      value='TESTE2',
# )