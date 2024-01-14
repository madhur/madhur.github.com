---
layout: blog-post
title: "Ways of traversing tree"
excerpt: "Ways of traversing tree"
disqus_id: /2021/02/10/ways-of-traversing-tree/
tags:
    - Tree
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
