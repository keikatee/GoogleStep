import sys
import collections
from collections import deque

class Wikipedia:

    # Initialize the graph of pages.
    def __init__(self, pages_file, links_file):

        # A mapping from a page ID (integer) to the page title.
        # For example, self.titles[1234] returns the title of the page whose
        # ID is 1234.
        self.titles = {}

        # A set of page links.
        # For example, self.links[1234] returns an array of page IDs linked
        # from the page whose ID is 1234.
        self.links = {}

        # Read the pages file into self.titles.
        with open(pages_file) as file:
            for line in file:
                (id, title) = line.rstrip().split(" ")
                id = int(id)
                assert not id in self.titles, id
                self.titles[id] = title
                self.links[id] = []
        print("Finished reading %s" % pages_file)

        # Read the links file into self.links.
        with open(links_file) as file:
            for line in file:
                (src, dst) = line.rstrip().split(" ")
                (src, dst) = (int(src), int(dst))
                assert src in self.titles, src
                assert dst in self.titles, dst
                self.links[src].append(dst)
        print("Finished reading %s" % links_file)
        print()

    # Example: Find the longest titles.
    def find_longest_titles(self):
        titles = sorted(self.titles.values(), key=len, reverse=True)
        print("The longest titles are:")
        count = 0
        index = 0
        while count < 15 and index < len(titles):
            if titles[index].find("_") == -1:
                print(titles[index])
                count += 1
            index += 1
        print()

    # Example: Find the most linked pages.
    def find_most_linked_pages(self):
        link_count = {}
        for id in self.titles.keys():
            link_count[id] = 0

        for id in self.titles.keys():
            for dst in self.links[id]:
                link_count[dst] += 1

        print("The most linked pages are:")
        link_count_max = max(link_count.values())
        for dst in link_count.keys():
            if link_count[dst] == link_count_max:
                print(self.titles[dst], link_count_max)
        print()

    def find_id_by_title(self, title):
        """Find id by id's title name"""
        for page_id, page_title in self.titles.items():
            if page_title == title:
                return page_id
        return None

    def find_path_from_goal(self, start_id, goal_id, previous):
        """Find the path from goal_id to the start_id."""
        path = []
        current = goal_id
        path.append(self.titles[current])
        while current != start_id and current in previous:
            current = previous[current]
            path.append(self.titles[current])
        path.reverse()#pathをreverseすることでstartからgoalのpathを得ることができる

        return path
    # Homework #1: Find the shortest path.
    # 'start': A title of the start page.
    # 'goal': A title of the goal page.

    def find_shortest_path(self, start, goal):
        """Find the shortest path from the page to the another pages."""
        queue = deque()
        visited = {}#今までに訪れたことのあるページを記録しておく
        previous = {}#訪れたページと次のページをペアにし保存する

        start_id = self.find_id_by_title(start) #startのタイトルよりページidを求める
        goal_id = self.find_id_by_title(goal) #goalのタイトルよりページidを求める

        if start_id is None or goal_id is None:#start_idやgoal_idが存在しない場合
            print("Start or goal is not in the page dictionary.")
            exit(1)

        visited[start_id] = True #はじめにstart_idをvisitedに追加
        queue.append(start_id) #queueにstart_idを入れる

        while queue:#queueが空でない場合
            current = queue.popleft()
            if current == goal_id:#今のnodeがgoal_idと一致した場合break
                break
            for neighbour in self.links[current]:#今のnodeから飛べるページ(neighbour)について調べる
                if neighbour not in visited:
                    visited[neighbour] = True
                    previous[neighbour] = current#previousにneighbourとcurrentをペアにして追加する
                    queue.append(neighbour)

        if goal_id in previous:
            print(" -> ".join(self.find_path_from_goal(start_id, goal_id, previous)))
        else:
            print("Not found")

        pass


    # Homework #2: Calculate the page ranks and print the most popular pages.
    def find_most_popular_pages(self):
        """Find most popular pages from the wikipedia pages."""
        old_page_rank = {}  # 元々のページランク
        new_page_rank = {}  # 更新用のページランク

        for title in self.titles:
            old_page_rank[title] = 1
            new_page_rank[title] = 0

        page_rank_updated = True

        while page_rank_updated:#page_rank_updatedの条件を満たす場合（True)の時while loopを回し続ける
            for title in self.titles:
                new_page_rank[title] = 0 #更新用のページランクを０にする

            all_rank_share = 0 #全てのidのrankを変更する関数

            for node_id in self.links:
                if len(self.links[node_id]) != 0:
                    rank_share = old_page_rank[node_id] * 0.85 / len(self.links[node_id])
                    all_rank_share += 0.15 * old_page_rank[node_id]
                    for to_id in self.links[node_id]:
                        new_page_rank[to_id] += rank_share

                else:
                    all_rank_share += old_page_rank[node_id]
            changes = 0 #new_page_rank[title] - old_page_rank[title]の差を求める関数
            for title in self.titles:
                new_page_rank[title] += all_rank_share / len(self.titles)
                changes += (new_page_rank[title] - old_page_rank[title]) ** 2

            if changes < 0.01:
                page_rank_updated = False #changesの値が0.01以下になったらFalseにしwhile loopを止める

            old_page_rank = new_page_rank.copy() #0.1以下でない場合old_page_rankをnew_page_rankの値に変更する
            print(changes)

        sorted_pages = sorted(new_page_rank.items(), key=lambda x: x[1], reverse=True)
        print("The most popular pages are:")
        index = min(10, len(self.titles))#最もpopularな10ページまたはそれ以下のindexを登録
        for id, rank in sorted_pages[:index]:
            print(f"{self.titles[id]}: {rank:.4f}")


        pass


    # Homework #3 (optional):
    # Search the longest path with heuristics.
    # 'start': A title of the start page.
    # 'goal': A title of the goal page.
    def find_longest_path(self, start, goal):
        #------------------------#
        # Write your code here!  #
        #------------------------#
        pass


    # Helper function for Homework #3:
    # Please use this function to check if the found path is well formed.
    # 'path': An array of page IDs that stores the found path.
    #     path[0] is the start page. path[-1] is the goal page.
    #     path[0] -> path[1] -> ... -> path[-1] is the path from the start
    #     page to the goal page.
    # 'start': A title of the start page.
    # 'goal': A title of the goal page.
    def assert_path(self, path, start, goal):
        assert(start != goal)
        assert(len(path) >= 2)
        assert(self.titles[path[0]] == start)
        assert(self.titles[path[-1]] == goal)
        for i in range(len(path) - 1):
            assert(path[i + 1] in self.links[path[i]])



if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("usage: %s pages_file links_file" % sys.argv[0])
        exit(1)

    wikipedia = Wikipedia(sys.argv[1], sys.argv[2])
    # Example
    wikipedia.find_longest_titles()
    # Example
    wikipedia.find_most_linked_pages()
    # Homework #1
    wikipedia.find_shortest_path("渋谷", "パレートの法則")
    # Homework #2
    wikipedia.find_most_popular_pages()
    # Homework #3 (optional)
    wikipedia.find_longest_path("渋谷", "池袋")

