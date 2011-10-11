from model.Terminal import Terminal

class TerminalHelper(object):
    
    @classmethod
    def get_terminals(self, airport):
        terminals = {}
        terminals = Terminal.get_terminal_info_by_terminal(airport)
        
        if not terminals:
            return ApiResponse.TERMINAL_NOT_FOUND
        else:
            for airline in terminals:
                del airline[Terminal.A_OBJECT_ID]
            return terminals
