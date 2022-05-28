# Othello.xdc

Othello/Reversi game implemented as webXdc app.

<img width=300 src=https://user-images.githubusercontent.com/9800740/170844337-ea1b94f0-fbe6-4b43-ad14-d9b9ba0ae3bc.png>

[Download .xdc from Release Assets](https://github.com/webxdc/Othello.xdc/releases), attach to a Delta Chat group and play othello/reversi with a group member!

## Requirements

This project depends on:
- [Python 3](https://python.org/)
- [Transcrypt](https://www.transcrypt.org/)

Once you have Python installed execute:

```sh
python -m pip install -r ./requirements.txt
```

## Building

```sh
python ./build.py
```

The output is a file with `.xdc` extension.

## Testing

After building, you are ready to test the app. The project comes with an
small simulator that allows to test your app in your browser, to do it
just go to the root of the project and run this command:

```sh
python -m http.server
```

then open in your browser the URL that is displayed in the shell.

## Credits

Inspired by: https://codepen.io/hac-kimagure/pen/KLyWow

## License

Licensed GPLv3+, see the LICENSE file for details.

Copyright © 2022  Asiel Díaz Benítez.
