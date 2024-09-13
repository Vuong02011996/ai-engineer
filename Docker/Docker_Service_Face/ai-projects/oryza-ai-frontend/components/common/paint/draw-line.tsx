import React, { useRef, useState, useEffect } from "react";
import { PainToolbar } from "./toolbar";
import { TypeServiceKey } from "@/constants/type-service";

interface Point {
  x: number;
  y: number;
}

export interface IPainLineComponentProps {
  image: string;
  onReloadImage: () => void;
  onSubmit: (lines: any) => void;
  lines?: string;
  type?: TypeServiceKey;
}

export const DrawLineComponenent = (props: IPainLineComponentProps) => {
  const service_applied = [
    TypeServiceKey.tripwire,
    TypeServiceKey.plate_number,
    TypeServiceKey.obj_attr
  ]
  const canvasRef = useRef<any>(null);
  const boxRef = useRef<HTMLDivElement | null>(null);
  const [points, setPoints] = useState<Point[]>([]);
  const [dragging, setDragging] = useState(false);
  const [dragIndex, setDragIndex] = useState<any>(null);
  const [draggingShape, setDraggingShape] = useState(false);
  const [image, setImage] = useState<any>(null);
  const [isPen, setIsPen] = useState(true);
  const [lockNewPoint, setLockNewPoint] = useState(false);

  const handleCanvasClick = (event: any) => {
    if (draggingShape) {
      setdrag(true);
      const rect = canvasRef.current.getBoundingClientRect();
      const x = event.clientX - rect.left;
      const y = event.clientY - rect.top;
      setOffset({ x, y });
      return;
    }
    if (!isPen || !image) return;

    const rect = canvasRef.current.getBoundingClientRect();
    const x = event.clientX - rect.left;
    const y = event.clientY - rect.top;

    // Check if clicking near an existing point to start dragging
    for (let i = 0; i < points.length; i++) {
      const point = points[i];
      if (Math.abs(point.x - x) < 10 && Math.abs(point.y - y) < 10) {
        setDragIndex(i);
        setDragging(true);
        return;
      }
    }
    if (lockNewPoint) return;
    const newPoints = [...points, { x, y }];
    setPoints(newPoints);
    handleSubmit(newPoints);
    setDragIndex(newPoints.length - 1);
  };

  const drawLine = (root: Point, arrow: Point) => {
    const context = canvasRef.current.getContext("2d");
    context.beginPath();
    context.moveTo(root.x, root.y);
    context.lineTo(arrow.x, arrow.y);
    context.strokeStyle = "#9C0000";
    context.lineWidth = 3;
    context.stroke();
  };

  const handleMouseMove = (event: any) => {
    if (draggingShape && drag) {
      const rect = canvasRef.current.getBoundingClientRect();
      const x = event.clientX - rect.left;
      const y = event.clientY - rect.top;

      const dx = x - offset.x;
      const dy = y - offset.y;

      setPoints(points.map((point) => ({ x: point.x + dx, y: point.y + dy })));
      handleSubmit(
        points.map((point) => ({ x: point.x + dx, y: point.y + dy }))
      );

      setOffset({ x, y });
      return;
    }

    if (!dragging) return;

    const rect = canvasRef.current.getBoundingClientRect();
    const x = event.clientX - rect.left;
    const y = event.clientY - rect.top;
    const newPoints = [...points];
    newPoints[dragIndex] = { x, y };
    setPoints(newPoints);
    console.log('point', newPoints)
    handleSubmit(newPoints);
  };

  const handleMouseUp = () => {
    if (draggingShape) {
      setdrag(false);
      return;
    }
    setDragging(false);
  };

  const handleImageUpload = (event: any) => {
    if (event) {
      const file = event.target.files[0];
      if (!file) return;
      const img = new Image();
      img.onload = () => {
        setImage(img);
        const canvas = canvasRef.current;

        const MAX_WIDTH = boxRef.current?.clientWidth || 400;
        const ratio = img.width / img.height;

        const width = img.width > MAX_WIDTH ? MAX_WIDTH : img.width;
        const height = img.width > MAX_WIDTH ? MAX_WIDTH / ratio : img.height;
        canvas.width = width;
        canvas.height = height;
      };
      img.src = URL.createObjectURL(file);
    } else {
      // load existed settings and image
      const img = new Image();
      img.onload = () => {
        setImage(img);
        const canvas = canvasRef.current;

        const MAX_WIDTH = boxRef.current?.clientWidth || 400;
        const ratio = img.width / img.height;

        const width = img.width > MAX_WIDTH ? MAX_WIDTH : img.width;
        const height = img.width > MAX_WIDTH ? MAX_WIDTH / ratio : img.height;

        canvas.width = width;
        canvas.height = height;

        if (props.lines) {
          console.log('go here lines', props.lines)
          try {
            const existed_points = [];
            let lines = JSON.parse(props.lines);
            // here it defaultly load lines, 
            // so we need to check if it is tripwire, we need to wrap it in array
            if (props.type && service_applied.includes(props.type)) {
              lines = [lines];
              setLockNewPoint(true);
            }
            console.log('Recently drawed line', lines)
            for (const line of lines) {
                const p1 = line[0];
                const p2 = line[1];
                existed_points.push(
                  { x: p1[0] * width, y: p1[1] * height },
                  { x: p2[0] * width, y: p2[1] * height }
                );
            }
            setPoints(existed_points);
          } catch (error) {
            console.error('Failed to parse lanes:', error);
            console.log('Received lines:', props.lines);
          }
        }
      }

      img.src = props.image ?? "/images/img-mock.jpg";
    }
  };

  useEffect(() => {
    handleImageUpload(null);
  }, [props.image]);

  useEffect(() => {
    const canvas = canvasRef.current;
    const context = canvas.getContext("2d");
    context.clearRect(0, 0, canvas.width, canvas.height);

    if (image) {
      context.drawImage(image, 0, 0, canvas.width, canvas.height);
    }

    if (points.length >= 2) {
      for (let i = 0; i < points.length; i += 2) {
        if (i + 1 >= points.length) break;

        const root = points[i];
        const arrow = points[i + 1];

        // Draw the vector (arrow)
        drawLine(root, arrow);
      }
    }
    if (points.length < 2) {
      setLockNewPoint(false);
    }

    // Draw the points for visual feedback
    points.forEach((point, index) => {
      context.beginPath();
      context.arc(point.x, point.y, 10, 0, 2 * Math.PI);
      context.fillStyle = dragIndex === index ? "red" : "#007DC0";
      context.fill();
    });
  }, [points, image, dragIndex]);

  const [offset, setOffset] = useState<any>({ x: 0, y: 0 });
  const [drag, setdrag] = useState(false);

  // * * * * * * * * * * * * * * * * *
  const handleSubmit = (points: Point[]) => {
    console.log('submit line', points)
    if (points.length % 2 !== 0) return;
    console.log('submit line')
    let lines = [];
    let line = [];
    const MAX_WIDTH = boxRef.current?.clientWidth || 400;
    const ratio = image.width / image.height;

    const width = image.width > MAX_WIDTH ? MAX_WIDTH : image.width;
    const height = image.width > MAX_WIDTH ? MAX_WIDTH / ratio : image.height;

    for (const key in points) {
      const point = points[key];
      const x = point.x / width;
      const y = point.y / height;

      line.push([x, y]);
      if (line.length === 2) {
        lines.push(line);
        line = [];
        // if tripwire, only need 1 line
        if (props.type && service_applied.includes(props.type)) {
          setLockNewPoint(true);
        }
      }
      
    }
    console.log(lines)
    if (props.type && service_applied.includes(props.type)) {
      props.onSubmit(JSON.stringify(lines[0]));
      return;
    }
    props.onSubmit(JSON.stringify(lines));
  };

  return (
    <div>
      <div className="relative">
        <PainToolbar
          onMove={() => {
            setDraggingShape(!draggingShape);
            setIsPen(false);
          }}
          onPaint={() => {
            setIsPen(true);
            setDraggingShape(false);
          }}
          onRemove={() => {
            setPoints((prev) => prev.filter((v, i) => i !== dragIndex));
            setDragIndex(points.length - 2);
            handleSubmit(points.filter((v, i) => i !== dragIndex));
          }}
          onReset={() => {
            setPoints([]);
            handleSubmit([]);
          }}
          // isShowSubmit={points.length >= 3 && isPen}
          onSubmit={() => {
            handleSubmit(points);
            setIsPen(false);
          }}
          onRefresh={props.onReloadImage}
        />
        <div ref={boxRef}>
          <canvas
            ref={canvasRef}
            onMouseMove={handleMouseMove}
            onMouseDown={handleCanvasClick}
            onMouseUp={handleMouseUp}
          />
        </div>
      </div>
      {/* <div className="flex flex-row items-center  py-1 justify-between">
        <p className="text-[#323232] text-[14px] font-medium ">
          Vị trí điểm chọn
        </p>
        <div className="flex flex-row space-x-3 ">
          {_renderInputValue({
            label: "X",
            value: dragIndex && points[dragIndex]?.x,
            onKeyDown: (e) => {
              if (dragIndex && e.code === "Enter") {
                const newPoints = [...points];
                const x = Number(e.currentTarget.value);
                const y = newPoints[dragIndex].y;
                newPoints[dragIndex] = { x, y };
                setPoints(newPoints);
              }
            },
          })}
          {_renderInputValue({
            label: "Y",
            value: dragIndex && points[dragIndex]?.y,
            onKeyDown: (e) => {
              if (dragIndex && e.code === "Enter") {
                const newPoints = [...points];
                const x = newPoints[dragIndex].x;
                const y = Number(e.currentTarget.value);
                newPoints[dragIndex] = { x, y };
                setPoints(newPoints);
              }
            },
          })}
        </div>
      </div> */}
    </div>
  );
};
// function _renderInputValue({
//   label,
//   value,
//   onKeyDown,
// }: {
//   label: string;
//   value: string;
//   onKeyDown: (e: any) => void;
// }) {
//   return (
//     <div className="flex flex-row items-center space-x-2 ">
//       <p className="text-[#808080] text-[14px] font-normal uppercase">
//         {label}
//       </p>
//       <input
//         defaultValue={value}
//         onKeyDown={onKeyDown}
//         type="text"
//         placeholder="-"
//         className="w-14 border border-[#E3E5E5] rounded-md outline-none text-center py-[6px] text-grayOz font-medium text-[14px]"
//       />
//     </div>
//   );
// }
