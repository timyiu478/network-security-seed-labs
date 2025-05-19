
for name in ${names[@]}; do
   dockerID=$(docker ps | grep $name | awk '{print $1}')

   if [[ ! -f ${name}_bird.conf ]]; then
       echo "Copy bird.conf from the container: $name"
       docker cp $dockerID:/etc/bird/bird.conf ${name}_bird.conf
   else 
       echo "** File ${name}_bird.conf already exists; will not overwrite."
   fi
done
