import requests
import re
import sys
from time import sleep


def ncbi_blast(blast, sequence):
    base_url = 'https://blast.ncbi.nlm.nih.gov/blast/Blast.cgi'
    megablast = 'on' if blast == 'blastn' else 'off'
    post_params = {
        'CMD': 'put',
        'PROGRAM': blast,
        'MEGABLAST': megablast,
        'DATABASE': 'nr',
        'QUERY': sequence,
    }
    post_response = requests.post(base_url, params=post_params)
    print("Status Code is", post_response.status_code)

    pattern = r'RID = ([^\\n]*)\\n'
    search_rid = re.search(pattern, str(post_response.content))
    rid = search_rid.group(1)
    print("RequestID is", rid)

    while(True):
        sleep(5)

        check_params = {
            'CMD': 'Get',
            'FORMAT_OBJECT': 'SearchInfo',
            'RID': rid,
        }
        check_response = requests.get(base_url, params=check_params)
        str_check_response = str(check_response.content)

        if re.search("Status=WAITING", str_check_response):
            print("waiting now...")
            continue

        if re.search("Status=FAILED", str_check_response):
            print("Search failed...\n")
            break

        if re.search("Status=UNKNOWN", str_check_response):
            print("something happened...\n")
            break

        if re.search("Status=READY", str_check_response):
            if re.search("hereAreHits=yes", str_check_response):
                print("BLAST search finished.")
                
                get_params = {
                    'CMD': 'Get',
                    'FORMAT_TYPE': 'Text',
                    'RID': rid,
                }
                get_response = requests.get(base_url, params=get_params)
                f = open("{0}.txt".format(rid), 'w')
                f.write(get_response.text)
                f.close()
                print(get_response.text)
                break
            else:
                print("No hits found...\n")
                break


if __name__ == "__main__":
    sequence = 'GTTCGAGAGGTGTGCTCTGAACAAGCCGAGACGGGGCCGTGCCGAGCAATGATCTCCCGCTGGTACTTTGATGTGACTGAAGGGAAGTGTGCCCCATTCTTTTACGGCGGATGTGGCGGCAACCGGAACAACTTTGACACAGAAGAGTACTGCATGGCCGTGTGTGGCAGCGCCATGTCCCAAAGTTTACTCAAGACTACCCAGGAACCTCTTGCCCGAGATCCTGTTAAACTTCCTACAACA'
    ncbi_blast('blastx', sequence)
