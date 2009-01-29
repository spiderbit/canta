find . -name "*.py" |while read line
do

echo $line

# change ident from tab -> 4 spaces
#expand -t 4 -i $line > $line.new
#mv $line.new $line

# add a empty line + a vi modeline
#echo "" >> $line
#echo "# vim: ai ts=4 sts=4 et sw=4" >> $line

done