# Format result to a table.
#
class Formatter:
    title_and_head = ""
    contents = ""

    def __init__(self, separator="+", headers="|", content="|"):
        self.separator = separator
        self.headers = headers
        self.content = content

    def formatted_output(self, titleName, header, content_list):
        """Returns a formatted string.
        """
        header = formatTabLine(header)
        for i in range(0, len(content_list)):
            content_list[i] = formatTabLine(content_list[i])
            if len(header) != len(content_list[i]):
                return "WARN: column numbers are different, please check your config and json files."
        info_max = []
        none_list = []
        total_length = len(content_list[0]) - 1 - len(titleName)
        # when the header var contains '\n', split and get length
        for h in header:
            none_list.append(None)
            headerMaxLength = 0
            hs = str(h)
            if hs.__contains__("\n"):
                headerList = hs.split("\n")
                for h2 in headerList:
                    headerMaxLength = len(h2) if len(h2) > len(headerList[0]) else len(headerList[0])
            else:
                headerMaxLength = len(h)
            info_max.append(headerMaxLength)
        # get max length list: info_max
        for info_i in content_list:
            for k in range(0, len(info_i), 1):
                # solve: when line feed, do split
                info_k = str(info_i[k]).split("\n")
                for ik in info_k:
                    if info_max[k] < len(ik):
                        info_max[k] = len(ik)

        self.headers = formatFeedLines(self.headers, header, info_max, none_list)
        for im in info_max:
            self.separator += "-" * im + "+"
            total_length += im
        if total_length % 2 == 0:
            title = "|" + " " * int(total_length / 2) + titleName + " " * int(total_length / 2) + "|"
        else:
            title = "|" + " " * int(total_length / 2) + titleName + " " * int(total_length / 2 + 1) + "|"
        first_line = "+" + "-" * int(total_length + int(len(titleName))) + "+"

        self.title_and_head = first_line + "\n" + title + "\n" + self.separator + "\n" + self.headers + "\n" + self.separator

        # print first_line
        # print head_and_title
        # print self.separator
        # print self.headers
        # print self.separator

        for info in content_list:
            self.content = formatFeedLines(self.content, info, info_max, none_list)
            self.contents += "\n" + self.content + "\n" + self.separator
            # print self.content
            self.content = "|"
            # print self.separator
        return self.title_and_head + self.contents

def formatFeedLines(line, info, info_max, none_list):
    """When line feed or contains '\n', do as below."""
    next_line_content = []
    flag = "false"
    for i in range(0, len(info)):
        if "\n" in str(info[i]):
            flag = "true"
            splits = info[i].split("\n")
            line += splits[0] + " " * (info_max[i] - len(splits[0])) + "|"
            splits.pop(0)
            next_line_content.append(splits)
        else:
            next_line_content.append(None)
            line += str(info[i]) + " " * (info_max[i] - len(str(info[i]))) + "|"
    while flag == "true":
        line += "\n|"
        for i in range(0, len(next_line_content)):
            if next_line_content[i] is None:
                line += " " * info_max[i] + "|"
            else:
                line += next_line_content[i][0] + " " * (info_max[i] - len(next_line_content[i][0])) + "|"
                next_line_content[i].pop(0)
                if len(next_line_content[i]) == 0:
                    next_line_content[i] = None
            if next_line_content == none_list:
                flag = "false"
    return line

def formatTabLine(info):
    """When line contains '\t', replace it using four [SPACE]."""
    for i in range(0, len(info)):
        info[i] = str(info[i]).replace("\t", " " * 4)
    return info
