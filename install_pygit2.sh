# Source this from bash
echo "Downloading and building libgit2"
wget https://github.com/libgit2/libgit2/archive/v0.22.0.tar.gz
tar xzf v0.22.0.tar.gz
cd libgit2-0.22.0/
cmake . && make && sudo make install
cd ..
rm -rf libgit2-0.22.0/
rm v0.22.0.tar.gz
echo "Installing pygit2"
sudo pip install pygit2 || (echo "Linking issue, trying ldconfig" && sudo ldconfig)
sudo pip install pygit2 && python -c 'import pygit2' && echo "Success!"
