import React, { useRef, useState, useEffect } from "react";
import { PainToolbar } from "./toolbar";
// import { TypeServiceKey } from "@/constants/type-service";

interface Point {
  x: number;
  y: number;
}

export interface IPainLaneComponentsProps {
  image: string;
  onReloadImage: () => void;
  onSubmit: (lanes: any) => void;
  lanes?: string;
  // type?: TypeServiceKey;
}

export const DrawLaneComponent = (props: IPainLaneComponentsProps) => {
  const canvasRef = useRef<any>(null);
  const boxRef = useRef<HTMLDivElement | null>(null);
  const [points, setPoints] = useState<Point[]>([]);
  const [dragging, setDragging] = useState(false);
  const [dragIndex, setDragIndex] = useState<any>(null);
  const [draggingShape, setDraggingShape] = useState(false);
  const [image, setImage] = useState<any>(null);
  const [isPen, setIsPen] = useState(true);

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
    const newPoints = [...points, { x, y }];
    setPoints(newPoints);
    handleSubmit(newPoints);
    setDragIndex(newPoints.length - 1);
  };

  const drawArrow = (root: Point, arrow: Point) => {
    const context = canvasRef.current.getContext("2d");
    context.beginPath();
    context.moveTo(root.x, root.y);
    context.lineTo(arrow.x, arrow.y);
    context.strokeStyle = "#78C6E7";
    context.lineWidth = 3;
    context.stroke();
    
    // Draw arrowhead (simple version)
    const headlen = 10; // length of head in pixels
    const angle = Math.atan2(arrow.y - root.y, arrow.x - root.x);
    context.beginPath();
    context.moveTo(arrow.x, arrow.y);
    context.lineTo(
      arrow.x - headlen * Math.cos(angle - Math.PI / 6),
      arrow.y - headlen * Math.sin(angle - Math.PI / 6)
    );
    context.lineTo(
      arrow.x - headlen * Math.cos(angle + Math.PI / 6),
      arrow.y - headlen * Math.sin(angle + Math.PI / 6)
    );
    context.lineTo(arrow.x, arrow.y);
    context.lineTo(
      arrow.x - headlen * Math.cos(angle - Math.PI / 6),
      arrow.y - headlen * Math.sin(angle - Math.PI / 6)
    );
    context.strokeStyle = "#f60002";
    context.lineWidth = 5;
    context.stroke();
    context.fillStyle = "#f60002";
    context.fill();
  };

  const drawConnectionLines = (
    root1: Point,
    root2: Point,
    arrow1: Point,
    arrow2: Point
  ) => {
    const context = canvasRef.current.getContext("2d");
    context.beginPath();
    context.moveTo(root1.x, root1.y);
    context.lineTo(root2.x, root2.y);
    context.lineTo(arrow2.x, arrow2.y);
    context.lineTo(arrow1.x, arrow1.y);
    context.closePath();
    context.fillStyle = "rgba(241, 46, 233, 0.50)";
    context.fill();

    context.strokeStyle = "#78C6E7";
    context.lineWidth = 1;
    context.stroke();

    return context;
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
    // console.log('point', newPoints)
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

        if (props.lanes) {
          // console.log('go here lanes', props.lanes)
          try {
            const existed_points = [];
            const lanes = JSON.parse(props.lanes);
            // console.log('lanes', lanes)
            for (const lane of lanes) {
              for (const line of lane) {
                const root = line[0];
                const arrow = line[1];
                existed_points.push(
                  { x: root[0] * width, y: root[1] * height },
                  { x: arrow[0] * width, y: arrow[1] * height }
                );
              }
            }
            setPoints(existed_points);
          } catch (error) {
            console.error('Failed to parse lanes:', error);
            console.log('Received lanes:', props.lanes);
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
        drawArrow(root, arrow);

        if (i >= 2 && i % 4 !== 0) {
          const prevRoot = points[i - 2];
          const prevArrow = points[i - 1];
          drawConnectionLines(prevRoot, root, prevArrow, arrow);
        }
      }
    }

    // Draw the points for visual feedback
    points.forEach((point, index) => {
      context.beginPath();
      context.arc(point.x, point.y, 10, 0, 2 * Math.PI);
      context.fillStyle = dragIndex === index ? "red" : "#007DC0";
      context.fill();
    });
    // console.log('points', points)
  }, [points, image, dragIndex]);

  const [offset, setOffset] = useState<any>({ x: 0, y: 0 });
  const [drag, setdrag] = useState(false);

  // * * * * * * * * * * * * * * * * *
  const handleSubmit = (points: Point[]) => {
    // console.log('submit lane', points)
    if (points.length % 4 !== 0) return;
    // console.log('submit lane')
    let result = [];
    let lane = [];
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
        lane.push(line);
        if (lane.length === 2) {
          result.push(lane);
          lane = [];
        }
        line = [];
      }
      
    }
    console.log(result)
    props.onSubmit(JSON.stringify(result));
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
      <div className="flex flex-row items-center  py-1 justify-between">
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
      </div>
    </div>
  );
};
function _renderInputValue({
  label,
  value,
  onKeyDown,
}: {
  label: string;
  value: string;
  onKeyDown: (e: any) => void;
}) {
  return (
    <div className="flex flex-row items-center space-x-2 ">
      <p className="text-[#808080] text-[14px] font-normal uppercase">
        {label}
      </p>
      <input
        defaultValue={value}
        onKeyDown={onKeyDown}
        type="text"
        placeholder="-"
        className="w-14 border border-[#E3E5E5] rounded-md outline-none text-center py-[6px] text-grayOz font-medium text-[14px]"
      />
    </div>
  );
}
