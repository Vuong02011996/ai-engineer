import React, { useRef, useState, useEffect } from "react";
import { PainToolbar } from "./toolbar";
import { TypeServiceKey } from "@/constants/type-service";
interface Point {
  x: number;
  y: number;
}

export interface IPainComponentsProps {
  image: string;
  onReloadImage: () => void;
  onSubmit: (boundary: any) => void;
  points?: string;
  type?: TypeServiceKey;
  drawLine?: boolean;
}

export const PainComponents = (props: IPainComponentsProps) => {
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
      console.log("down");
      setOffset({ x, y });
      return;
    }
    if (!isPen) return;
    if (!image) return;

    const rect = canvasRef.current.getBoundingClientRect();
    const x = event.clientX - rect.left;
    const y = event.clientY - rect.top;

    // Check if clicking near an existing point to start dragging
    for (let i = 0; i < points.length; i++) {
      const point = points[i];
      if (Math.abs(point.x - x) < 5 && Math.abs(point.y - y) < 5) {
        setDragIndex(i);
        setDragging(true);
        return;
      }
    }

    if (props.drawLine && points.length >= 2) {
      return;
    }

    if (props.type === TypeServiceKey.plate_number) {
      if (points.length < 2) {
        setPoints((prevPoints) => [...prevPoints, { x, y }]);
        handleSubmit([...points, { x, y }]);
        setDragIndex(points.length);
      }
    } else {
      setPoints((prevPoints) => [...prevPoints, { x, y }]);
      handleSubmit([...points, { x, y }]);
      setDragIndex(points.length);
    }

    if (props.drawLine) {
      if (points.length < 2) {
        const newPoints = [...points, { x, y }];
        setPoints(newPoints);
        handleSubmit(newPoints);
        setDragIndex(newPoints.length - 1);
      }
    } else {
      const newPoints = [...points, { x, y }];
      setPoints(newPoints);
      handleSubmit(newPoints);
      setDragIndex(newPoints.length - 1);
    }
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
    handleSubmit(newPoints);
  };

  const handleMouseUp = () => {
    if (draggingShape) {
      console.log("up");
      setdrag(false);
      return;
    }
    setDragging(false);
    // setDragIndex(null);
  };

  function convertPoint(pointArr: any, width: any, height: any) {
    if (pointArr) {
      let result: any = [];
      const points = JSON.parse(pointArr);

      for (const key in points) {
        const element = {
          x: points[key][0] * width,
          y: points[key][1] * height,
        };
        result.push(element);
      }
      return result;
    }

    return [];
  }

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

        // canvas.width = img.width;
        // canvas.height = img.height;
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

        if (props.points) {
          try {
            const point = convertPoint(props.points, width, height);
            setPoints(point);
          } catch (error) {
            console.log(error);
          }
        }
      };

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

    if (props.drawLine && points.length === 2) {
      context.beginPath();
      context.moveTo(points[0].x, points[0].y);
      context.lineTo(points[1].x, points[1].y);
      context.strokeStyle = "#f60002";
      context.lineWidth = 5;
      context.stroke();
    } else if (points.length >= 2) {
      context.beginPath();
      context.moveTo(points[0].x, points[0].y);
      for (let i = 1; i < points.length; i++) {
        context.lineTo(points[i].x, points[i].y);
      }
      context.closePath();
      context.fillStyle = "rgba(241, 46, 233, 0.50)";
      context.fill();
  
      context.strokeStyle = "#78C6E7";
      context.lineWidth = 1;
      context.stroke();
    }
  
    // Draw the points for visual feedback
    points.forEach((point, index) => {
      context.beginPath();
      context.arc(point.x, point.y, 5, 0, 2 * Math.PI);
      context.fillStyle = dragIndex === index ? "red" : "#007DC0";
      context.fill();
    });
    console.log("points", points);
  }, [points, image, dragIndex, props.drawLine]);

  const [offset, setOffset] = useState<any>({ x: 0, y: 0 });
  const [drag, setdrag] = useState(false);

  // * * * * * * * * * * * * * * * * *
  const handleSubmit = (points: Point[]) => {
    let result = [];
    const MAX_WIDTH = boxRef.current?.clientWidth || 400;
    const ratio = image.width / image.height;

    const width = image.width > MAX_WIDTH ? MAX_WIDTH : image.width;
    const height = image.width > MAX_WIDTH ? MAX_WIDTH / ratio : image.height;

    for (const key in points) {
      const point = points[key];
      const x = point.x / width;
      const y = point.y / height;

      result.push([x, y]);
    }
    console.log("result", result);
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
