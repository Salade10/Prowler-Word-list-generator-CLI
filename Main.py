#!/usr/bin/env python3
from itertools import product, permutations
import argparse

def run_main():
    # Substitution list
    default_leet = {
        'a': ['@', '4'],
        'e': ['3'],
        'i': ['1', '!'],
        'o': ['0'],
        's': ['$', '5'],
    }

    # Load the leet map, optionally overridden by CLI
    def load_leet_map(cli_overrides=None):
        leet = default_leet.copy()
        if cli_overrides:
            for kv in cli_overrides:
                if '=' in kv:
                    k, v = kv.split('=', 1)
                    leet[k.lower()] = [v]
        return leet

    # Generate all case permutations
    def generate_case_permutations(word, prefix='', suffix='', irs=None, irp=None):
        if irs is None:
            irs = ['']
        if irp is None:
            irp = ['']
        
        #The list where the final words are stored
        variants = []

        
        if not word.endswith(".txt"):

            states = list(product([0, 1], repeat=len(word)))
            # Normalize irp
            if isinstance(irp,str) and irp.endswith(".txt"):
                with open(irp, 'r') as f:
                    irp_list = f.read().splitlines()
            else:
                irp_list = list(irp or '')  # turn "12" into ['1', '2']

            # Normalize irs
            if isinstance(irs,str) and irs.endswith(".txt"):
                with open(irs, 'r') as f:
                    irs_list = f.read().splitlines()
            else:
                irs_list = list(irs or '')

            # Now process all variants
            for suffix_item in irs_list:
                for prefix_item in irp_list:
                    for state in states:
                        new_word = ''
                        for i, bit in enumerate(state):
                            new_word += word[i].upper() if bit else word[i].lower()
                        full_variant = prefix_item + prefix + new_word + suffix + suffix_item
                        variants.append(full_variant)
        #Allows for -w to have a file as an arg
        else:

            #Open the file that has been passed
            with open(word, 'r') as wordfile:
                words=wordfile.read().splitlines()


                # Normalize irp
                if isinstance(irp,str) and irp.endswith(".txt"):
                    with open(irp, 'r') as f:
                        irp_list = f.read().splitlines()
                else:
                    irp_list = list(irp or '')  # turn "12" into ['1', '2']

                # Normalize irs
                if isinstance(irs,str) and irs.endswith(".txt"):
                    with open(irs, 'r') as f:
                        irs_list = f.read().splitlines()
                else:
                    irs_list = list(irs or '')

                # Now process all variants
                for word in words:
                    states = list(product([0, 1], repeat=len(word)))
                    for suffix_item in irs_list:
                        for prefix_item in irp_list:
                            for state in states:
                                new_word = ''
                                for i, bit in enumerate(state):
                                    new_word += word[i].upper() if bit else word[i].lower()
                                full_variant = prefix_item + prefix + new_word + suffix + suffix_item
                                variants.append(full_variant)
                        
        return variants

    # Apply leetspeak to a list of words
    def generate_leet_variants(words, leet_map):
        all_variants = []
        for word in words:
            chars = []
            for c in word:
                variants = [c]
                if c.lower() in leet_map:
                    variants.extend(leet_map[c.lower()])
                chars.append(variants)
            all_variants.extend([''.join(p) for p in product(*chars)])
        return all_variants

    # Argparse config
    parser = argparse.ArgumentParser(description="Generate case and leet variants of a word.")
    parser.add_argument('-w', '--word', required=True, help='The base word')
    parser.add_argument('-o', '--output', help='File to write output')
    parser.add_argument('-p', '--prefix', default='', help='Optional prefix')
    parser.add_argument('-s', '--suffix', default='', help='Optional suffix')
    parser.add_argument('-l', '--leet', action='store_true', help='Enable leetspeak substitutions')
    parser.add_argument('-ls', '--leetsub', nargs='*', help='Override default leet map (ex: e=3 s=$)')
    parser.add_argument('-irp', '--incrandprefix', nargs='?', help='include random prefix')
    parser.add_argument('-irs', '--incrandsuffix', nargs='?', help='include random prefix')
    parser.add_argument('-ca', '--customargument', help='allows to manually insert where a symbol,letter or number would go')

    args = parser.parse_args()

    # Create variants
    case_variants = generate_case_permutations(args.word, args.prefix, args.suffix, args.incrandsuffix, args.incrandprefix)


    #Debug SCRIPT##
    if args.customargument:    
        states =[''.join(p) for p in permutations(args.customargument)]
        print(states)

    # Apply leet if requested
    if args.leet:
        leet_map = load_leet_map(args.leetsub)
        all_variants = generate_leet_variants(case_variants, leet_map)
    else:
        all_variants = case_variants

    # Output results
    if args.output:
        with open(args.output, 'a') as f:
            for variant in all_variants:
                f.write(variant + '\n')
    else:
        for variant in all_variants:
            print(variant)
            
            
def start():
    run_main()

parser = argparse.ArgumentParser(description="Generate case and leet variants of a word.")
parser.add_argument('--prowler' required=True)
parser.set_defaults(func=lambds args: start(args) if args.prowler else None)
