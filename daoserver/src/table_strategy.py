"""
Module to contain table allocation strategy
"""

class ProtestAvoidanceStrategy(object):
    """
    Allocate tables by determining all possible options and allocating based on
    fewest protests.

    Algorithm:
        Protest:
            - Assume a game has two entrants (who have a history of tables
            played on)
            - When a table is proposed one, or both, entrants may protest
            - This gives a protest score of 0, 1, 2 (no-protest -> both protest)
        Layout:
            - A layout is a single possible configuration of entrants on
            tables. Essentially this is one candidate for final configuration.
        Allocation:
            - For all possible layouts, determine the aggregate protest
            - The least protested layout is chosen
        Variations:
            - There are four obvious variations:
                - Avoid double protests - Least Outrage
                - Avoid single protests - split happy and sad (perhaps good for
                the competitive tables where playing there before-hand is a
                real advantage)
                - Avoid no protests - least variety
                - Lowest aggregate protest - Utility happiness
        Time-complexity:
            - n3 for n games
        Memory Complexity:
            - 4 * n3 integers for n games.
        Potential Trade-off:
            A reasonably complex select to get table history for each player
            could be stored with the entry.
    """

    @staticmethod
    def get_protest_score_for_game(table, entries):
        """
        Get the protest score for a single game.
        Returns a single protest score between 0 and len(entries)
        Expects:
            - an int for the table number
            - A list of Entry
        """
        protests = 0
        table = int(table)
        for entry in entries:
            if table in entry.game_history:
                protests += 1
        return protests

    @staticmethod
    def get_protest_score_for_layout(layout):
        """
        Get the protest scores for a single layout

        Expects:
            List of tuples [(table, [entries at that table])]
            Note that the game might simply be the string 'BYE'
        Returns:
            A list of protests [
                0-protest-count,
                1-protest-count,
                2-protest-count,
                total-protest-points,
                ]
        """
        if len(layout) == 0:
            return [0, 0, 0, 0]
        num_entries = len(layout[0][1])
        if any(len(x[1]) != num_entries for x in layout):
            raise IndexError('Some games have differing numbers of entries')

        protest_list = [0 for x in range(num_entries + 2)] # pylint: disable=W0612
        for game in layout:
            g1 = game[1][0]
            g2 = game[1][1]

            if g1 == 'BYE' or g2 == 'BYE':
                protests = 0
            else:
                protests = ProtestAvoidanceStrategy.get_protest_score_for_game(
                    game[0], (g1, g2))
            protest_list[protests] += 1
            protest_list[-1] += protests

        return protest_list
