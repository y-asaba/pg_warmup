import sys
from os import devnull
from optparse import OptionParser
from subprocess import check_output, call

from pg_warmup.relation import (
    Relation, RelationNotFoundException,
    RelationFileAccessDeniedException
)


def main():
    parser = OptionParser()
    parser.add_option('-t', '--table', dest='table', type="string", help="warmup the named table")
    parser.add_option('-d', '--database', dest='database', type="string", help="dbname")
    parser.add_option('-i', action='store_true', dest='use_ionice',
                      default=False, help="use ionice command")
    parser.add_option('-s', action='store_true', dest='use_shared_buffer',
                      default=False, help="cache on shared buffer, not page cache")
    parser.add_option('-x', action='store_false', dest='dryrun',
                      default=True, help="execute warmup")

    (options, args) = parser.parse_args()
    try:
        if options.database is None:
            print("Please specify a database name using -d option")
            sys.exit(1)

        if options.table is None:
            print("Please specify a table name using -t option")
            sys.exit(1)

        if options.use_ionice:
            #
            # Check if ionice is installed
            #
            with open(devnull, "w") as fnull:
                try:
                    ret = call(['ionice', '-h'], stdout=fnull, stderr=fnull)
                    if ret != 0:
                        print("ionice is not installed. Please install ionice or run pg_warmup without -i option")
                        sys.exit(1)
                except Exception as ex:
                    #
                    # In python 3.3, FileNotFoundException will be occured.
                    # In python 2.7, OSError will be occured.
                    #
                    print("ionice is not installed. Please install ionice or run pg_warmup without -i option")
                    sys.exit(1)

        relation = Relation.get_relation(options.database, options.table)
        relation.print_relation()
        relation.warmup(use_shared_buffer=options.use_shared_buffer, use_ionice=options.use_ionice, dryrun=options.dryrun)
        if options.dryrun:
            print("\033[31m!! This is a dry run. Please specify -x option to warmup !!\033[0m")

    except RelationNotFoundException:
        print("ERROR: \"%s\" table does not exist" % options.table)
        sys.exit(1)

    except RelationFileAccessDeniedException:
        print("ERROR: Cannot access files of \"%s\" table" % options.table)
        sys.exit(1)
    

if __name__ == '__main__':
    main()
