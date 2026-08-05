export default function Loading({ color, size }) {
  const style = {
    backgroundColor: '#6ca6fd',
    width: 40,
    height: 40,
  };

  if (color !== undefined) {
    style.color = color;
  }
  if (size !== undefined) {
    style.width = size;
    style.height = size;
  }

  return <div className="bouncer" style={style} />;
}
