HISTFILE=/data/.bash_history
set -o vi

alias ll='ls -l'
alias lt='ls -lt'
alias ltr='ls -ltr'
alias ltm='ls -lt | more'
alias gs='git status'
alias gl='git log'
alias gls='git log -n1 && \
           echo && \
           echo "====================================================================" && \
           echo && \
           git status'
