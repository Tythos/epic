# Passes all arguments to the command-line Python entry point
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
python $DIR/../command.py $@
