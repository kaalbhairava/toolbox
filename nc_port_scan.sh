#!/bin/sh

nargs=$#
help_msg="This is help message | my.sh ip_file port_file out_file tor |
mention tor in argument if you want anonymous scan |
for that you first need to configure tor and proxychains"
if [ "$nargs" -eq 0 ]
then
	echo "type my.sh -h to print the help message"
	exit 1

elif [ "$nargs" -eq 1 ]
then
	for arg in "$@"
	do
		if [ "$arg"=="-h" ] || [ "$arg"=="--help" ]
		then
			echo "$help_msg"
			exit 1
		fi
	done
elif [ "$nargs" -gt 2 ] 
then
	in_f="$1"
	p_f="$2"
	out_f="$3"
	anon="$4"
	echo "$anon"

	date >> $out_f
	for ip in $(cat "$in_f")
	do
		for p in $(cat "$p_f")
		do
			sleep 1
			if test -z "$anon"
			then
				nc -v -C -z -w 3 $ip $p
			elif test "$anon" = "tor"
			then
				proxychains nc -v -C -z -w 3 $ip $p
			fi
		done >> $out_f 2>&1
	done
else
	echo "$help_msg"
fi
