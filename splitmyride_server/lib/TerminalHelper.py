from model.Terminal import Terminal
from lib import ApiResponse

class TerminalHelper(object):
    
    @classmethod
    def get_terminals(self, airport):
        terminals = Terminal.get_terminal_info_by_airport(airport)
        if not terminals:
            return ApiResponse.TERMINAL_NOT_FOUND
        else:
            return terminals
