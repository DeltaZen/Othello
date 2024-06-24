# Othello

Othello/Reversi game implemented as webXdc app.

## Contributing

### Requirements

This project depends on:
- [Python 3](https://python.org/)
- [Transcrypt](https://www.transcrypt.org/)

Once you have Python installed execute:

```sh
python -m pip install -r ./requirements.txt
```

### Building

```sh
python ./build.py
```

The output is a file with `.xdc` extension.

### Testing

After building, you are ready to test the app. The project comes with an
small simulator that allows to test your app in your browser, to do it
just go to the root of the project and run this command:

```sh
python -m http.server
```

then open in your browser the URL that is displayed in the shell.

### Releasing

To automatically build and create a new GitHub release with the `.xdc` file:

```
git tag -a v1.0.1
git push origin v1.0.1
```

## Credits

Inspired by: https://codepen.io/hac-kimagure/pen/KLyWow
