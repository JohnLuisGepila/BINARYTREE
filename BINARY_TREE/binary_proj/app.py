from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

class BinaryTree:
    def __init__(self):
        self.root = None
    
    def insert(self, value):
        if not self.root:
            self.root = Node(value)
            return
        
        queue = [self.root]
        while queue:
            current = queue.pop(0)
            if not current.left:
                current.left = Node(value)
                return
            else:
                queue.append(current.left)
            if not current.right:
                current.right = Node(value)
                return
            else:
                queue.append(current.right)

    def traverse(self, order_type):
        result = []
        
        def preorder(node):
            if node:
                result.append(str(node.value))
                preorder(node.left)
                preorder(node.right)
        
        def inorder(node):
            if node:
                inorder(node.left)
                result.append(str(node.value))
                inorder(node.right)
        
        def postorder(node):
            if node:
                postorder(node.left)
                postorder(node.right)
                result.append(str(node.value))
        
        if order_type == 'preorder':
            preorder(self.root)
        elif order_type == 'inorder':
            inorder(self.root)
        elif order_type == 'postorder':
            postorder(self.root)
            
        return result

    def search(self, target):
        if not self.root:
            return False
            
        queue = [self.root]
        while queue:
            current = queue.pop(0)
            if str(current.value) == str(target):
                return True
            if current.left:
                queue.append(current.left)
            if current.right:
                queue.append(current.right)
        return False

    def get_tree_structure(self, node, level=0):
        if not node:
            return []
        result = [{"value": node.value, "level": level}]
        if node.left:
            result.extend(self.get_tree_structure(node.left, level + 1))
        if node.right:
            result.extend(self.get_tree_structure(node.right, level + 1))
        return result

binary_tree = BinaryTree()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/insert', methods=['POST'])
def insert_value():
    data = request.get_json()
    try:
        value = data['value'].strip()
        if not value:
            return jsonify({"success": False, "error": "Please enter a value"})
        
        binary_tree.insert(value)
        tree_structure = binary_tree.get_tree_structure(binary_tree.root)
        
        return jsonify({
            "success": True, 
            "tree": tree_structure,
            "traversals": {
                "preorder": binary_tree.traverse('preorder'),
                "inorder": binary_tree.traverse('inorder'),
                "postorder": binary_tree.traverse('postorder')
            }
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

@app.route('/search', methods=['POST'])
def search_value():
    data = request.get_json()
    try:
        value = data['value'].strip()
        if not value:
            return jsonify({"success": False, "error": "Please enter a value to search"})
        
        found = binary_tree.search(value)
        return jsonify({
            "success": True,
            "found": found,
            "message": "Match found!" if found else "No match found."
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

@app.route('/clear', methods=['POST'])
def clear_tree():
    try:
        global binary_tree
        binary_tree = BinaryTree()
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

if __name__ == '__main__':
    app.run(debug=True)