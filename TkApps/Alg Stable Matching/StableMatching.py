import tkinter as tk
from tkinter import messagebox


class FuncVarsAlg:
    def __init__(self):
        self.free_players = []
        self.expected_contract = []

    def begin_matching(self, player_ranked_teams, team_ranked_players):
        self.free_players = [player for player in player_ranked_teams.keys()]

        while len(self.free_players) > 0:
            for player in self.free_players:
                self.stable_matching(player, player_ranked_teams, team_ranked_players)

        self.matching_result()

    def stable_matching(self, player, player_ranked_teams, team_ranked_players):
        for team in player_ranked_teams[player]:
            # checks if team is already taken or not
            taken_match = [contract for contract in self.expected_contract if team in contract]
            if len(taken_match) == 0:
                self.expected_contract.append([player, team])
                self.free_players.remove(player)
                break
            elif len(taken_match) > 0:
                # compares rankings of current and potential players
                current_player = team_ranked_players[team].index(player)
                potential_player = team_ranked_players[team].index(taken_match[0][0])
                if current_player < potential_player:
                    self.free_players.remove(player)
                    self.free_players.append(taken_match[0][0])
                    taken_match[0][0] = player
                    break

    def matching_result(self):
        result_list = self.expected_contract
        result_str = "Stable Matching Results:\n\n"
        for i in range(len(result_list)):
            result_str += (result_list[i])[0] + " --> " + (result_list[i])[1] + "\n"
        messagebox.showinfo(None, result_str)


class GUI(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.configure(bg="lightblue", relief="groove", bd=4)
        self.pack(expand=1, fill="both")
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, pad=10)
        self.grid_rowconfigure(1, pad=10)
        self.grid_rowconfigure(2, pad=10)
        self.grid_rowconfigure(3, pad=10)
        self.grid_rowconfigure(4, pad=10)

        tk.Label(self, text="Group 1\nmembers", font="bold", bg="lightblue").grid(padx=4, row=0, column=0)
        self.gp1_txt = tk.Text(self, height=2, width=85, bg="azure", bd=2)
        self.gp1_txt.grid(row=0, column=1)
        self.gp1_txt.focus()

        tk.Label(self, text="Group 2\nmembers", font="bold", bg="lightblue").grid(row=1, column=0)
        self.gp2_txt = tk.Text(self, height=2, width=85, bg="azure", bd=2)
        self.gp2_txt.grid(row=1, column=1)

        tk.Label(self, text="Prefs for\nGroup 1\nmembers", font="bold", bg="lightblue").grid(row=2, column=0)
        self.pref1_txt = tk.Text(self, height=12, width=85, bg="azure", bd=2)
        self.pref1_txt.grid(row=2, column=1)

        tk.Label(self, text="Pref-lists\nfor\nGroup 2\nmembers", font="bold", bg="lightblue").grid(row=3, column=0)
        self.pref2_txt = tk.Text(self, height=12, width=85, bg="azure", bd=2)
        self.pref2_txt.grid(row=3, column=1)

        tk.Button(self, text="HELP", bg="khaki", bd=2, command=self.example_help).grid(row=4, column=0, pady=5)

        tk.Button(self, text="START MATCHING", bg="lightgreen", bd=2, command=lambda: self.get_inputs(
            self.gp1_txt.get("1.0", "end-1c"), self.gp2_txt.get("1.0", "end-1c"),
            self.pref1_txt.get("1.0", 'end-1c'), self.pref2_txt.get("1.0", 'end-1c'))
        ).grid(row=4, column=1, columnspan=1, pady=5)

    def example_help(self):
        gp1val = "PLAYER1,PLAYER2,PLAYER3,PLAYER4"
        gp2val = "TEAM1,TEAM2,TEAM3,TEAM4"
        pref1val = "TEAM1,TEAM2,TEAM3,TEAM4\n" \
                   "TEAM2,TEAM1,TEAM4,TEAM3\n" \
                   "TEAM2,TEAM4,TEAM3,TEAM1\n" \
                   "TEAM1,TEAM2,TEAM3,TEAM4"
        pref2val = "PLAYER1,PLAYER3,PLAYER2,PLAYER4\n" \
                   "PLAYER1,PLAYER3,PLAYER4,PLAYER2\n" \
                   "PLAYER4,PLAYER2,PLAYER1,PLAYER3\n" \
                   "PLAYER1,PLAYER2,PLAYER4,PLAYER3"

        self.gp1_txt.delete("1.0", "end")
        self.gp2_txt.delete("1.0", "end")
        self.pref1_txt.delete("1.0", "end")
        self.pref2_txt.delete("1.0", "end")

        self.gp1_txt.insert("end", gp1val)
        self.gp2_txt.insert("end", gp2val)
        self.pref1_txt.insert("end", pref1val)
        self.pref2_txt.insert("end", pref2val)

    def get_inputs(self, gp1, gp2, p1, p2):
        group1 = gp1.split(',')
        group2 = gp2.split(',')

        pref1 = []
        a = p1.split('\n')
        for i in a:
            k = i.split(',')
            pref1.append(k)

        pref2 = []
        a = p2.split('\n')
        for i in a:
            k = i.split(',')
            pref2.append(k)

        validres = self.send_valid_input(group1, group2, pref1, pref2)
        if validres == "OK":

            player_ranked_teams = {pl: pref1[i] for i, pl in enumerate(group1)}
            team_ranked_players = {tm: pref2[i] for i, tm in enumerate(group2)}
            FuncVarsAlg.begin_matching(FuncVarsAlg(), player_ranked_teams, team_ranked_players)

            '''
            5 rows in 1 :))
            team_ranked_players = {}
            i = 0
            for tm in group2:
                team_ranked_players.update({tm: pref2[i]})
                i += 1
            '''

    @staticmethod
    def send_valid_input(grp1, grp2, pref1, pref2):
        if len(grp1) != len(grp2):
            messagebox.showerror(None, 'Lengths of Groups are unequal!')
        elif len(pref1[0]) != len(pref1):
            messagebox.showerror(None, 'Invalid Preference 1 matrix!')
        elif len(pref2[0]) != len(pref2):
            messagebox.showerror(None, 'Invalid Preference 2 matrix!')
        else:
            return "OK"


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Stable Matching Algorithm")
    root.geometry("800x600")
    root.resizable(0, 0)
    root.config(cursor="hand1")
    GUI(root)
    FuncVarsAlg()
    root.mainloop()
