---
layout: blog-post
title: "Rofi Process Killer"
excerpt: "Rofi Process Killer"
disqus_id: /2025/11/01/rofi-process-killer/
tags:
    - Rofi
---

> **Disclaimer**: This blog article has been generated with the assistance of AI to help announce and explain the features of Rofi Process Killer. While the content is AI-generated, the software itself and the ideas behind it are the result of real development work and genuine user needs.

# Introducing Rofi Process Killer: A Better Way to Manage Linux Processes

Ever found yourself hunting through `htop` or typing `ps aux | grep` just to kill a misbehaving process? If you're a Linux user who loves efficient workflows, I've got something that might change how you handle process management forever.

Today, I'm excited to announce **Rofi Process Killer** – a sleek, keyboard-driven process manager that integrates seamlessly with the popular rofi application launcher.

## What is Rofi Process Killer?

Rofi Process Killer is a custom rofi module that transforms process management from a command-line chore into an intuitive, visual experience. With just a few keystrokes, you can:

- **View all running processes** with complete command lines, CPU usage, and memory consumption
- **Kill processes instantly** with intelligent graceful termination (SIGTERM) followed by force kill (SIGKILL) if needed
- **See full command arguments** – no more truncated process names
- **Filter processes in real-time** using rofi's built-in search capabilities

## Why I Built This

As someone who frequently works with multiple development environments, Docker containers, and various system processes, I was constantly frustrated by the traditional process management workflow:

1. Open terminal
2. Run `ps aux` or `htop`
3. Search for the problematic process
4. Note down the PID
5. Kill it with `kill` command

This felt clunky, especially when using tiling window managers where quick, keyboard-driven actions are paramount. I wanted something that felt as smooth as launching applications with rofi – and that's exactly what this tool delivers.

## Key Features

### **Complete Process Information**
Unlike basic process viewers, Rofi Process Killer shows you everything you need:
- Process ID (PID)
- CPU usage percentage
- Memory usage percentage  
- Process owner
- **Full command line with all arguments** (no truncation!)

### **Smart Text Wrapping**
Long command lines don't get cut off – they wrap intelligently across multiple lines, so you can see exactly what each process is doing.

### **Safe Process Termination**
The tool follows best practices for process management:
1. First attempts graceful termination (SIGTERM)
2. If the process doesn't respond, automatically escalates to force kill (SIGKILL)
3. Provides desktop notifications for feedback

### **Beautiful Dark Theme**
Includes a custom rofi theme optimized for process management with:
- Clean, readable monospace font
- Dark color scheme that's easy on the eyes
- Proper spacing for wrapped text
- Visual distinction between normal and selected processes

## Installation

### For Arch Linux Users
```bash
# Install from AUR 
yay -S rofi-process-killer

# Or install manually from GitHub
git clone https://github.com/madhur/rofi-process-killer.git
cd rofi-process-killer
chmod +x rofi-process-killer.sh
cp rofi-process-killer.sh ~/.local/bin/
cp process-killer.rasi ~/.config/rofi/themes/
```

### Usage
Launch with a simple command:
```bash
rofi -modi "processes:rofi-process-killer" -show processes -theme ~/.config/rofi/themes/process-killer.rasi
```

Or create a keyboard shortcut in your window manager:
```bash
# i3/sway example
bindsym $mod+Shift+p exec rofi -modi "processes:rofi-process-killer" -show processes
```

## Perfect for Power Users

This tool shines in environments where efficiency matters:

- **Tiling Window Managers**: i3, sway, bspwm, etc.
- **Development Workflows**: Quickly kill runaway dev servers, Docker containers, or build processes
- **System Administration**: Fast process management without leaving your current workspace
- **General Productivity**: Any scenario where you need quick access to process management

## Technical Implementation

For those curious about the internals, the tool is built as a rofi script mode that:

- Uses `ps auxww` with unlimited width to capture complete command lines
- Implements intelligent process filtering to exclude kernel threads
- Provides error handling for permission-denied scenarios
- Integrates with the desktop notification system for user feedback

The custom rofi theme leverages advanced CSS-like styling to enable text wrapping and optimize the visual layout for process information.

## What's Next?

I'm already working on several enhancements:

- **Process filtering options** (by user, CPU usage, memory usage)
- **Process tree view** to show parent-child relationships
- **Resource usage graphs** for visual process monitoring
- **Integration with systemd** for service management
- **Configuration file** for customizable display options

## Try It Today

Ready to streamline your process management workflow? 

**🔗 GitHub Repository**: https://github.com/madhur/rofi-process-killer

The repository includes:
- Complete installation instructions
- Usage examples and screenshots
- Custom theme files
- Keyboard shortcut configurations for popular window managers

## Contributing

This is an open-source project, and I welcome contributions! Whether you want to:
- Report bugs or suggest features
- Improve the documentation
- Add new functionality
- Create additional themes

Feel free to open issues or submit pull requests on GitHub.

## Final Thoughts

Rofi Process Killer represents what I love about the Linux ecosystem – the ability to create tools that perfectly fit your workflow. It's fast, efficient, and keyboard-driven, embodying the Unix philosophy of doing one thing well.

If you're someone who appreciates well-crafted developer tools and efficient workflows, give it a try. I think you'll find it becomes an indispensable part of your daily Linux experience.

---

*Have you tried Rofi Process Killer? I'd love to hear your feedback! Connect with me on [GitHub](https://github.com/madhur) or share your experience in the comments below.*

**Tags**: #Linux #Rofi #ProcessManagement #OpenSource #ProductivityTools #TilingWindowManagers #Developer Tools