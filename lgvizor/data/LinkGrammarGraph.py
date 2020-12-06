import urllib.request as request
import numpy as np

from lgvizor.rendering.helpers import get_colored_pen


class LinkGrammarGraph:
    def __init__(self):

        self.category_words = {}
        self.category_rules = {}
        self.rule_connectors = {}

        self.words = set()
        self.categories = set()
        self.rules = set()
        self.connectors = set()

        self.positions = {
            'words': {},
            'clusters': {},
            'rules': {},
            'connectors': {}
        }

        self.layout_offset = 10
        self.link_width = 1
        self.node_size = 1

    def parse_cluster(self, cluster: str, words: list, rules: list):
        self.category_words[cluster] = words
        self.category_rules[cluster] = rules

        for rule in rules:
            self.rule_connectors[rule] = rule.split('&')
            self.connectors |= set(rule.replace('-', '').replace('+', '').split('&'))

        self.words |= set(words)
        self.categories.add(cluster)
        self.rules |= set(rules)

    def serialize(self,width_factor=1, height_factor=1):
        # We are generating:
        # (1) array of nodes positions [(x1, y1), ...]
        # (2) array of edges connecting nodes with indices in (1) array [(1, 7), ...]
        # (3) array of edge colors for each edge in the order of edge definition in (2)

        width_factor = 0.5 if width_factor <= 0.5 else width_factor
        height_factor = 0.5 if height_factor <= 0.5 else height_factor

        w_step = self.layout_offset * width_factor
        h_step = 2 * self.node_size * height_factor

        graph_height = max(len(self.words), len(self.categories), len(self.rules), len(self.connectors))

        nodes_positions = []
        label_texts = []
        edges = []
        edge_colors = []

        serialized_words_pos = {}
        serialized_categories_pos = {}
        serialized_rules_pos = {}
        serialized_connectors_pos = {}

        current_pos_idx = 0
        word_idx = 0
        category_idx = 0
        rule_idx = 0
        con_idx = 0

        for category in self.category_words:
            h_offset = category_idx * h_step * (graph_height - 1) / (len(self.categories) - 1)
            w_offset = 1 * w_step
            category_pos = [w_offset, h_offset]

            nodes_positions.append(category_pos)
            label_texts.append(category)

            serialized_categories_pos[category] = current_pos_idx

            category_idx += 1
            current_pos_idx += 1

            for word in self.category_words[category]:
                if word not in serialized_words_pos:
                    h_offset = word_idx * h_step * (graph_height - 1) / (len(self.words) - 1)
                    w_offset = 0
                    word_pos = [w_offset, h_offset]
                    nodes_positions.append(word_pos)
                    label_texts.append(word)
                    edges.append([current_pos_idx, serialized_categories_pos[category]])
                    serialized_words_pos[word] = current_pos_idx
                    current_pos_idx += 1
                    word_idx += 1
                else:
                    edges.append([serialized_words_pos[word], serialized_categories_pos[category]])

                edge_colors.append(get_colored_pen('s', self.link_width))

            for rule in self.category_rules[category]:
                if rule not in serialized_rules_pos:
                    h_offset = rule_idx * h_step * (graph_height - 1) / (len(self.rules) - 1)
                    w_offset = 2 * w_step
                    rule_pos = [w_offset, h_offset]
                    nodes_positions.append(rule_pos)
                    label_texts.append(rule)
                    edges.append([current_pos_idx, serialized_categories_pos[category]])
                    serialized_rules_pos[rule] = current_pos_idx
                    current_pos_idx += 1
                    rule_idx += 1
                else:
                    edges.append([serialized_rules_pos[rule], serialized_categories_pos[category]])

                edge_colors.append(get_colored_pen('green', self.link_width))

                for connector in self.rule_connectors[rule]:
                    if connector[:-1] not in serialized_connectors_pos:
                        h_offset = con_idx * h_step * (graph_height - 1) / (len(self.connectors) - 1)
                        w_offset = 3 * w_step
                        connector_pos = [w_offset, h_offset]
                        nodes_positions.append(connector_pos)
                        label_texts.append(connector[:-1])
                        edges.append([current_pos_idx, serialized_rules_pos[rule]])
                        serialized_connectors_pos[connector[:-1]] = current_pos_idx
                        current_pos_idx += 1
                        con_idx += 1
                    else:
                        edges.append([serialized_connectors_pos[connector[:-1]], serialized_rules_pos[rule]])

                    if connector[-1] == '-':
                        edge_colors.append(get_colored_pen('blue', self.link_width))
                    else:
                        edge_colors.append(get_colored_pen('red', self.link_width))

        nodes_positions = np.array(nodes_positions)
        label_texts = np.array(label_texts)
        edges = np.array(edges, dtype=np.uint)
        edge_colors = np.array(edge_colors, dtype=[
            ('red', np.ubyte),
            ('green', np.ubyte),
            ('blue', np.ubyte),
            ('alpha', np.ubyte),
            ('width', np.float)])

        return nodes_positions, edges, edge_colors, self.node_size, label_texts

    def parse_dictionary(self, lg_dictionary_url):
        response = request.urlopen(lg_dictionary_url)
        text = response.read().decode('utf-8')
        lines = text.split('\n')

        for i, block in enumerate(lines):
            if '% C' in block:
                cluster = lines[i].replace('% ', '').replace('\n', '')
                cluster_words = lines[i + 1].replace(':\n', '').replace('"', '').split(' ')
                rules = lines[i + 2].replace(';\n', '')\
                    .replace(';', '')\
                    .replace('(', '')\
                    .replace(')', '')\
                    .replace(' & ', '&')\
                    .split(' or ')

                self.parse_cluster(cluster, cluster_words, rules)
