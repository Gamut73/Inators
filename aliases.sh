scripts_dir="$HOME/Artificery/Inators"

function create_scripts_aliases() {
    for dir in ${scripts_dir}/*; do
        if [ -d "${dir}" ]; then
            dir_name=$(basename "${dir}")
            lower_dir_name=$(echo "${dir_name}" | tr '[:upper:]' '[:lower:]')
            alias "${lower_dir_name}"="python3 ${scripts_dir}/${lower_dir_name}/${lower_dir_name}.py"
        fi
    done
}
create_scripts_aliases


alias eiga="cd ~/Videos/Eiga"
alias series="cd ~/Videos/Series"
alias anime="cd ~/Videos/Anime"
