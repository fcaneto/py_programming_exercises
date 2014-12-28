"""
Problem Statement
    
Mr. Dengklek lives in the Kingdom of Ducks, where humans and ducks live together in peace and harmony.  Mr. Dengklek works as a chain maker. Today, he would like to make a beautiful chain as a decoration for one of his lovely ducks. He will produce the chain from leftovers he found in his workshop. Each of the leftovers is a chain piece consisting of exactly 3 links. Each link is either clean or rusty. Different clean links may have different degrees of beauty.  You are given a tuple (string) chains describing the leftovers. Each element of chains is a 3-character string describing one of the chain pieces. A rusty link is represented by a period ('.'), whereas a clean link is represented by a digit ('0'-'9'). The value of the digit in the clean link is the beauty of the link. For example, chains = {".15", "7..", "532", "..3"} means that Mr. Dengklek has 4 chain pieces, and only one of these ("532") has no rusty links.  All links have the same shape, which allows Mr. Dengklek to concatenate any two chain pieces. However, the link shape is not symmetric, therefore he may not reverse the chain pieces. E.g., in the above example he is able to produce the chain "532.15" or the chain ".15..37..", but he cannot produce "5323..".  To produce the chain, Mr. Dengklek will follow these steps:
Concatenate all chain pieces in any order.
Pick a contiguous sequence of links that contains no rusty links. Remove and discard all the remaining links.
The beauty of the new chain is the total beauty of all the links picked in the second step. Of course, Mr. Dengklek would like to create the most beautiful chain possible.  Return the largest possible beauty a chain can have according to the above rules.
Definition
    
Class:
DengklekMakingChains
Method:
maxBeauty
Parameters:
tuple (string)
Returns:
integer
Method signature:
def maxBeauty(self, chains):

Limits
    
Time limit (s):
2.000
Memory limit (MB):
64

Notes
-
Mr. Dengklek is not allowed to remove and discard individual links before concatenating the chain pieces.
-
If all links in the input are rusty, Mr. Dengklek is forced to select an empty sequence of links. The beauty of an empty sequence is 0.
Constraints
-
chains will contain between 1 and 50 elements, inclusive.
-
Each element of chains will contain exactly 3 characters.
-
Each character in each element of chains will be either a '.' or one of '0'-'9'.

"""
class CleanChain:
    def __init__(self, chain):
        self.value = int(chain[0]) + int(chain[1]) + int(chain[2])

class RustyChain:
    def __init__(self, chain):
        self.chain = chain
        self.head_value = self.get_value(head_value=True)
        self.tail_value = self.get_value()
        
        middle_link_value = int(chain[1]) if chain[1] != '.' else 0
        self.value = max(self.head_value, self.tail_value, middle_link_value)

    def get_value(self, head_value=False):
        chain = self.chain
        if head_value: 
            chain = reversed(self.chain)
        v = 0
        for link in chain:
            if link == '.':
                break
            else:
                v += int(link)
        return v

    def __str__(self):
        return "%s (%s, %s)" % (self.chain, self.head_value, self.tail_value)


def is_clean(chain):
        for link in chain:
            if link == '.':
                return False
        return True

class DengklekMakingChains:

    def maxBeauty(self, chains):
        middle_candidates = []
        other_chains = []
        # tuples (chain, value) - value may be head or tail value
        head_candidate = None
        tail_candidate = None
        head_backup = None
        tail_backup = None

        max_single_chain = None

        for chain in chains:
            if is_clean(chain):
                chain = CleanChain(chain)
                middle_candidates.append(chain)
            else:
                chain = RustyChain(chain)
                other_chains.append(chain)

            if not max_single_chain or chain.value > max_single_chain.value:
                max_single_chain = chain

        for chain in other_chains:
            if not chain.head_value and not chain.tail_value:
                continue

            # compare heads
            if not head_candidate or chain.head_value > head_candidate.head_value:
                    head_backup = head_candidate
                    head_candidate = chain
            else:
                if not head_backup or chain.head_value > head_backup.head_value:
                    head_backup = chain

            # print("?) %s" % chain)

            #compare tails
            if not tail_candidate or chain.tail_value > tail_candidate.tail_value:
                    tail_backup = tail_candidate
                    tail_candidate = chain
            else:
                if not tail_backup or chain.tail_value > tail_backup.tail_value:
                    tail_backup = chain

        # special cases
        if head_candidate == tail_candidate:
            if head_backup and tail_backup:
                if head_candidate.head_value + tail_backup.tail_value > head_backup.head_value + tail_candidate.tail_value:
                    tail_candidate = tail_backup
                else:
                    head_candidate = head_backup
            elif head_backup:
                head_candidate = head_backup
            elif tail_backup:
                tail_candidate = tail_backup
            else:
                tail_candidate = None
            
        sum = 0
        for chain in middle_candidates:
            # print("> " + chain)
            sum += chain.value
        if head_candidate:
            # print("head = %s" % head_candidate.chain)
            sum += head_candidate.head_value
        if tail_candidate:
            # print("tail = %s" % tail_candidate.chain)
            sum += tail_candidate.tail_value

        if sum < max_single_chain.value:
            sum = max_single_chain.value

        return sum


"""
Test Cases:
'...'
sum is single chain with most value
no clean chains - sum is head+tail
no head or tail candidates
head == tail: no backups, or only one backup
"""

print("19 == %s?" % DengklekMakingChains().maxBeauty({".15", "7..", "402", "..3"}))
print("0 == %s?" % DengklekMakingChains().maxBeauty({"...", "..."}))
print("28 == %s?" % DengklekMakingChains().maxBeauty({"16.", "9.8", ".24", "52.", "3.1", "532", "4.4", "111"}))
print("7 == %s?" % DengklekMakingChains().maxBeauty({"..1", "3..", "2..", ".7."}))
print("58 == %s?" % DengklekMakingChains().maxBeauty(
    {"412", "..7", ".58", "7.8", "32.", "6..", "351", "3.9", "985", "...", ".46"}))
print("9 == %s?" % DengklekMakingChains().maxBeauty({"111", "111", "1..", "..1", ".9."}))






