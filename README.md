# Othello

Othello/Reversi game implemented as webXdc app.

## Contributing

### Requirements

This project depends on:
- [Python 3](https://python.org/)
- [Transcrypt](https://www.transcrypt.org/): install it with: `pip install -r ./requirements.txt`
- [pnpm](https://pnpm.io/) used for building the `.xdc` file and local emulator

Once you have all programs installed execute:

```sh
pnpm i
```

### Testing

To test your work in your browser (with hot reloading!) while developing:

```sh
pnpm start
```

### Building

To package the WebXDC file:

```
pnpm build
```

To package the WebXDC with developer tools inside to debug in Delta Chat, set the `NODE_ENV`
environment variable to "debug":

```
NODE_ENV=debug pnpm build
```

The resulting optimized `.xdc` file is saved in `dist-xdc/` folder.

### Releasing

To automatically build and create a new GitHub release with the `.xdc` file:

```
git tag -a v1.0.1
git push origin v1.0.1
```

## Credits

Inspired by: https://codepen.io/hac-kimagure/pen/KLyWow
