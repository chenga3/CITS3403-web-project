#!/usr/bin/env sh

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

cd $DIR || exit

if [[ "$OSTYPE" != "linux-gnu"* ]]; then
        echo "Yeetcode is meant for a GNU/Linux based system"
		exit 1
fi

case $1 in
	start*)
		if (ps aux | grep "[w]orker.py") &> /dev/null || (ps aux | grep "[f]lask") &> /dev/null; then
			echo "Already Running"
			exit 1
		fi
		if ! (sudo systemctl is-active --quiet redis.service); then
			if ! (sudo systemctl start redis.service); then
				echo "Failed to start redis.service"
				exit 1
			fi
		fi
		if ! (python3 worker.py &) || !(flask run >> log.txt 2>&1 &); then
			exit 1
		fi
		echo $(grep Running log.txt | tail -1 | cut -d ' ' -f 3-5) ;;
	stop*)
		
		if ! kill $(ps aux | grep "[w]orker.py" | awk '{print $2}') &> /dev/null || !(killall flask); then
			echo "Already Stopped (or Crashed)"
		fi
		if (sudo systemctl is-active --quiet redis.service); then
			if ! (sudo systemctl stop redis.service); then
				echo "Failed to stop redis.service"
				exit 1
			fi
		fi
		echo "Successfully Stopped" 
		exit 0;;
	*) echo "Usage ./yeetcode.sh [start/stop]";;
esac
