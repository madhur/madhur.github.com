@echo off
echo "Building Content"
call jekyll --no-server --no-auto

echo "Checking out master"
git checkout master


echo "Copying the updated content to root"
cp -r _site/* . && rm -rf _site/ && touch .nojekyll

echo "Adding the content"
git add .

echo "Updated content"
git commit -am "Updated content"

echo "Pushed content"
git push --all origin
