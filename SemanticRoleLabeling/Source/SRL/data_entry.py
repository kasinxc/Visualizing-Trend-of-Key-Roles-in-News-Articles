class DataEntry:
    def __init__(self, td, ai, tp):
        self.title_desc = td
        self.article_ids = ai
        self.topic_prob = tp

        self.words_count = dict()
        self.verbs = list() # list of labelInfos
        self.reduced_title_desc = td
        while '  ' in self.reduced_title_desc:
            self.reduced_title_desc = self.reduced_title_desc.replace('  ', ' ')

    def process_description(self, description):
        # zero-base
        left_bracket = 0
        labelInfos = list()

        while left_bracket < len(description) and description[left_bracket]:
            if description[left_bracket] == '[':
                li = labelInfo()
                j = left_bracket
                colon = -1
                while description[j] != ':' and description[j] != ']':
                    j+=1
                if description[j] == ':':
                    colon = j
                while description[j] != ']':
                    j+=1
                if description[j] == ']':
                    right_bracket = j

                # By the way, get words Count
                words = description[colon+2:right_bracket]
                if words in self.words_count:
                    self.words_count[words] += 1
                else:
                    self.words_count[words] = 1 

                if colon < 0:
                    li.setLabel('NULL')
                    li.setPos(left_bracket, right_bracket-left_bracket-1)
                    # remove right_bracket and left_bracket
                        # right_bracket+1 is because "] haha" => "haha"
                    description = description[:right_bracket] + description[right_bracket+1:]
                    description = description[:left_bracket] + description[left_bracket+1:]
                else:
                    li.setLabel(description[left_bracket+1:colon])
                    li.setPos(left_bracket, right_bracket+left_bracket-colon-1-1) # delete one white space between right_bracket and colon
                    # right_bracket+1 is because "... [V: bbb] haha" => "... [V: bbb haha" 
                    description = description[:right_bracket] + description[right_bracket+1:]
                    # colon+2 is because "... [V: bbb haha" => "... bbb haha"
                    description = description[:left_bracket] + description[colon+2:]

                description = description.replace('  ', ' ')
                left_bracket = li.end-1
                labelInfos.append(li)

            else:
                left_bracket+=1

        self.verbs.append(labelInfos)
        print("topic id: " + str(self.topic_order))

    def process_srl(self):
        self.verbs = list()
        for verb_description in self.srl['verbs']:
            self.process_description(verb_description['description'])

    def set_srl(self, srl):
        self.srl = srl
        if not self.srl['verbs']:
            return
        print(self.srl['verbs'][0]['description'])
        print(len(self.srl['verbs']))

        self.process_srl()
