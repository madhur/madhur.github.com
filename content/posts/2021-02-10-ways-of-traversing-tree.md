---
slug: "ways-of-traversing-tree"
title: Ways of traversing tree
date: '2021-02-10'
year: '2021'
month: '2021-02'
description: Ways of traversing tree
tags:
  - Tree
draft: false
params:
  disqus_id: /2021/02/10/ways-of-traversing-tree/
---

We all know standard way of traversing trees such as 
* InOrder
* PostOrder
* PreOrder


However, its good to know some other ways of traversing trees as well.


```java
 private boolean findNode(TreeNode node, TreeNode n, List<TreeNode> path) {
        path.add(node);

        if (node.val == n.val) {
            return true;
        }

        if (node.left != null) {
            return findNode(node.left, n, path);
        }
        if (node.right != null) {
            return findNode(node.right, n, path);
        }

        path.remove(path.size() - 1);
        return false;
    }
```

```java
 private boolean findNode(TreeNode node, TreeNode n, List<TreeNode> path) {
        path.add(node);

        if (node.val == n.val) {
            return true;
        }

        if (node.left != null && findNode(node.left, n path)) {
            return true;
        }
        if (node.right != null && findNode(node.right, n, path)) {
            return true;
        }

        path.remove(path.size() - 1);
        return false;
    }
```
