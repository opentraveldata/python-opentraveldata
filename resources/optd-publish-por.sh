#!/bin/bash

#
GH_DIR="${HOME}/dev/opentraveldata"
OPTD_DATA_DIR="/var/www/data/optd/por"
POR_PUBLIC="optd_por_public_all.csv"
POR_UNLC="optd_por_unlc.csv"
declare -a por_file_list=("${POR_PUBLIC}" "${POR_UNLC}")

#
TODAY_DATE="$(date +%Y-%m-%d)"

# Synchronize from the remote GitHub OPTD repository
# and copy the latest POR data file into the Web server public data directory
download_and_publish() {
  por_full_file="opentraveldata/${por_file}"
  por_zip_file="${por_file}.bz2"
  por_zip_full_file="${por_full_file}.bz2"
  pushd ${GH_DIR}
  echo "Downloading the latest changes from the OPTD GitHub repository..."
  git pull
  por_file_date="$(git log -1 --pretty=""format:%ci"" ${por_full_file} | cut -d' ' -f1,1 | cut -d'-' -f1-3)"
  echo "... done => last modification date of ${por_full_file}: ${por_file_date}"

  echo "Compressing ${por_full_file}..."
  bzip2 -k ${por_full_file}
  echo "... done => ${por_zip_full_file}"

  mkdir -p ${OPTD_DATA_DIR}/${por_file_date}
  mv ${por_zip_full_file} ${OPTD_DATA_DIR}/${por_file_date}/
  popd

  # Update the Web server public data directory
  pushd ${OPTD_DATA_DIR}
  unlink ${por_file}
  ln -s ${por_file_date}/${por_zip_file} ${por_zip_file}
  popd

  # Reporting
  echo "Content of ${OPTD_DATA_DIR}/${POR_PUBLIC_DATE}"
  ls -lFH ${OPTD_DATA_DIR}/${POR_PUBLIC_DATE}
}

# Download and publish POR data files
for por_file in "${por_file_list[@]}"
do
  download_and_publish
done

# Reporting
echo "Content of ${OPTD_DATA_DIR}"
ls -lFH ${OPTD_DATA_DIR}


