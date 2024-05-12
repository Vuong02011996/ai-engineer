# folder / - ubuntu 22.04
`bin  boot  dev  etc  home  lib  lib32  lib64  libx32  media  mnt  opt  proc  root  run  sbin  srv  sys  tmp  usr  var  workspace`
+ root <=> ~ folder
# folder opt 
`half  hpcx  mellanox  nvidia  proto  riva  tritonclient  tritonserver`
+ nvidia:
+ tritonclient
+ tritonserver

# folder nvidia
**deepstream**  **entrypoint.d**  **graph-composer**  nsight-compute  nsight-systems-cli  nvidia_entrypoint.sh
+ deepstream
+ graph-composer
+ entrypoint.d : `10-banner.txt  15-container-copyright.txt  50-gpu-driver-check.sh    51-gpu-sm-version-check.sh`

# folder deepstream
+ deepstream  
+ deepstream-6.4

**Care folder sources and samples**
    + sources: place to clone example deepstream python
    + samples: 
        + configs:
        + models:
        + streams: 

**TWO THIS FOLDERS IS DONG BO vs NHAU, mkdir/rm folder , both in the same**

+ deepstream:
  + LICENSE.txt 
  + README       
  + entrypoint.sh  
  + reference_graphs                    
  + **sources**       
  + update_rtpmanager.sh           
  + version
  + LicenseAgreement.pdf        
  + README.rhel  install.sh    
  + rtpjitterbuffer_eos_handling.patch  
  + tools         
  + user_additional_install.sh
  + NvidiaDeepStreamDevelopmentLicense.pdf 
  + bin         
  + lib          
  + **samples**
+ deepstream-6.4: 
`LICENSE.txt                             README       entrypoint.sh  reference_graphs                    sources       update_rtpmanager.sh                    version
LicenseAgreement.pdf                    README.rhel  install.sh     rtpjitterbuffer_eos_handling.patch  tools         user_additional_install.sh
NvidiaDeepStreamDevelopmentLicense.pdf  bin          lib            samples                             uninstall.sh  user_deepstream_python_apps_install.sh`

## folder deepstream the same with deepstream-6.4
### **1. Folder samples**: 
  + **configs**  
  + **models**  
  + prepare_classification_test_video.sh  
  + prepare_ds_triton_model_repo.sh  
  + prepare_ds_triton_tao_model_repo.sh 
  + **streams** 
  + triton_model_repo  
  + triton_tao_model_repo 
  + trtis_model_repo
#### 1. Folder configs:
  + deepstream-app 
  + deepstream-app-triton  
  + deepstream-app-triton-grpc 
  + tao_pretrained_models
##### deepstream-app:
        + `config_infer_primary.txt                 config_preprocess_sgie.txt                     source30_1080p_dec_infer-resnet_tiled_display_int8.txt
              config_infer_primary.yml                 config_tracker_IOU.yml                         source30_1080p_dec_infer-resnet_tiled_display_int8.yml
              config_infer_primary_endv.txt            config_tracker_NvDCF_accuracy.yml              source30_1080p_dec_preprocess_infer-resnet_tiled_display_int8.txt
              config_infer_secondary_vehiclemake.txt   config_tracker_NvDCF_max_perf.yml              source4_1080p_dec_infer-resnet_tracker_sgie_tiled_display_int8.txt
              config_infer_secondary_vehiclemake.yml   config_tracker_NvDCF_perf.yml                  source4_1080p_dec_infer-resnet_tracker_sgie_tiled_display_int8.yml
              config_infer_secondary_vehicletypes.txt  config_tracker_NvDeepSORT.yml                  source4_1080p_dec_infer-resnet_tracker_sgie_tiled_display_int8_gpu1.txt
              config_infer_secondary_vehicletypes.yml  config_tracker_NvSORT.yml                      source4_1080p_dec_preprocess_infer-resnet_preprocess_sgie_tiled_display_int8.txt
              config_mux_source30.txt                  source1_usb_dec_infer_resnet_int8.txt          sources_30.csv
              config_mux_source4.txt                   source2_1080p_dec_infer-resnet_demux_int8.txt  sources_4.csv
              config_preprocess.txt                    source2_dewarper_test.txt
              `
##### deepstream-app-triton:
        + `README                                                                      config_infer_secondary_plan_engine_vehicletypes.txt
              config_infer_peoplesemsegnet_shuffle_tao.txt                                config_infer_secondary_plan_engine_vehicletypes_preprocess.txt
              config_infer_plan_engine_preprocess.txt                                     config_preprocess.txt
              config_infer_plan_engine_primary.txt                                        config_preprocess_sgie.txt
              config_infer_primary_classifier_densenet_onnx.txt                           source1_1080p_dec_infer_peoplesemsegnet_shuffle.txt
              config_infer_primary_classifier_inception_graphdef_postprocessInDS.txt      source1_primary_classifier.txt
              config_infer_primary_classifier_inception_graphdef_postprocessInTriton.txt  source1_primary_detector.txt
              config_infer_primary_classifier_mobilenet_v1_graphdef.txt                   source1_primary_detector_peoplenet_transformer.txt
              config_infer_primary_detector_peoplenet_transformer_tao.txt                 source30_1080p_dec_infer-resnet_tiled_display_int8.txt
              config_infer_primary_detector_ssd_inception_v2_coco_2018_01_28.txt          source4_1080p_dec_infer-resnet_tracker_sgie_tiled_display_int8.txt
              config_infer_primary_detector_ssd_mobilenet_v1_coco_2018_01_28.txt          source4_1080p_dec_preprocess_infer-resnet_tracker_preprocess_sgie_tiled_display_int8.txt
              config_infer_secondary_plan_engine_vehiclemake.txt                          source4_1080p_dec_preprocess_infer-resnet_tracker_sgie_tiled_display_int8.txt
              config_infer_secondary_plan_engine_vehiclemake_preprocess.txt
              `
##### deepstream-app-triton-grpc
        + `README                                                          config_preprocess.txt
          config_infer_peoplesemsegnet_shuffle_tao.txt                    config_preprocess_sgie.txt
          config_infer_plan_engine_preprocess.txt                         source1_1080p_dec_infer_peoplesemsegnet_shuffle.txt
          config_infer_plan_engine_primary.txt                            source1_primary_detector_peoplenet_transformer.txt
          config_infer_primary_detector_peoplenet_transformer_tao.txt     source30_1080p_dec_infer-resnet_tiled_display_int8.txt
          config_infer_secondary_plan_engine_vehiclemake.txt              source4_1080p_dec_infer-resnet_tracker_sgie_tiled_display_int8.txt
          config_infer_secondary_plan_engine_vehiclemake_preprocess.txt   source4_1080p_dec_preprocess_infer-resnet_tracker_preprocess_sgie_tiled_display_int8.txt
          config_infer_secondary_plan_engine_vehicletypes.txt             source4_1080p_dec_preprocess_infer-resnet_tracker_sgie_tiled_display_int8.txt
          config_infer_secondary_plan_engine_vehicletypes_preprocess.txt
          `
##### tao_pretrained_models: Run Test with TAO MODEL IN HERE: `deepstream-app -c deepstream_app_source1_peoplenet.txt`
        + `README.md                                                            deepstream_app_source1_peoplenet.txt      efficientdet_d0_labels.txt  mrcnn_labels.txt          ssd_labels.txt
          deepstream_app_source1_classifier_models.txt                         deepstream_app_source1_peoplenet.yml      frcnn_labels.txt            multi_task_labels.txt     triton
          deepstream_app_source1_classifier_models.yml                         deepstream_app_source1_segmentation.txt   labels_dashcamnet.txt       nvinfer                   triton-grpc
          deepstream_app_source1_dashcamnet_vehiclemakenet_vehicletypenet.txt  deepstream_app_source1_segmentation.yml   labels_facedetectir.txt     peopleSegNet_labels.txt   triton_server.md
          deepstream_app_source1_dashcamnet_vehiclemakenet_vehicletypenet.yml  deepstream_app_source1_trafficcamnet.txt  labels_facenet.txt          peoplenet_test.sh         triton_server_grpc.md
          deepstream_app_source1_detection_models.txt                          deepstream_app_source1_trafficcamnet.yml  labels_peoplenet.txt        peoplenet_triton_test.sh  yolov3_labels.txt
          deepstream_app_source1_detection_models.yml                          detectnet_v2_labels.txt                   labels_trafficnet.txt       prepare_triton_models.sh  yolov4_labels.txt
          deepstream_app_source1_facedetectir.txt                              download_models.sh                        labels_vehiclemakenet.txt   retinanet_labels.txt      yolov4_tiny_labels.txt
          deepstream_app_source1_facedetectir.yml                              dssd_labels.txt                           labels_vehicletypenet.txt   source_tao_app.csv
          `
#### 2. Folder models:
+ Primary_Detector  
+ SONYC_Audio_Classifier  
+ Secondary_VehicleMake  
+ Secondary_VehicleTypes  
+ Segmentation  
+ tao_pretrained_models
##### tao_pretrained_models: download Tao pretrained model saved  in HERE
+ dashcamnet  detectnet_v2  dssd  efficientdet  facedetectir  **facenet**  frcnn  **peopleNet**  peopleSegNet  retinanet  ssd  trafficcamnet  **unet**  vehiclemakenet  vehicletypenet  yolov3  yolov4  yolov4-tiny
    + peopleNet
      + `labels.txt  nvinfer_config.txt  resnet34_peoplenet_int8.onnx  resnet34_peoplenet_int8.onnx_b1_gpu0_int8.engine  resnet34_peoplenet_int8.txt`
    + facenet
      + `int8_calibration.txt  model.etlt`
    + unet: 
      + `unet_cal.bin  unet_resnet18.onnx`
+ Primary_Detector
      + `cal_trt.bin  resnet18_trafficcamnet.etlt                      resnet18_trafficcamnet.etlt_b2_gpu0_int8.engine   resnet18_trafficcamnet.etlt_b4_gpu0_int8.engine
            labels.txt   resnet18_trafficcamnet.etlt_b1_gpu0_int8.engine  resnet18_trafficcamnet.etlt_b30_gpu0_int8.engine`
#### 3. Folder streams: VIDEO Example in HERE
    + `fisheye_dist.mp4       sample_1080p_h265.mp4  sample_720p.mp4        sample_cam6.mp4        sample_office.mp4  sample_qHD.mp4        sample_walk.mov        yoga.mp4
        pointcloud             sample_720p.h264       sample_720p_mjpeg.mp4  sample_cans_jpg.tbz2   sample_push.mov    sample_ride_bike.mov  sonyc_mixed_audio.wav
        sample_1080p_h264.mp4  sample_720p.jpg        sample_cam5.mp4        sample_industrial.jpg  sample_qHD.h264    sample_run.mov        yoga.jpg`
  + triton_model_repo:
    + `Primary_Detector       Secondary_VehicleTypes   Segmentation_Semantic  inception_graphdef  ssd_inception_v2_coco_2018_01_28
        Secondary_VehicleMake  Segmentation_Industrial  densenet_onnx          mobilenet_v1        ssd_mobilenet_v1_coco_2018_01_28`
  + triton_tao_model_repo: `Primary_Detector  facenet  peoplenet_transformer  peoplesemsegnet_shuffle`
  + trtis_model_repo:
    + `Primary_Detector       Secondary_VehicleTypes   Segmentation_Semantic  inception_graphdef  ssd_inception_v2_coco_2018_01_28
        Secondary_VehicleMake  Segmentation_Industrial  densenet_onnx          mobilenet_v1        ssd_mobilenet_v1_coco_2018_01_28`


### **2. Folder sources**:
**CLONE Deepstream python apps in HERE** `deepstream_python_apps`
+ SONYCAudioClassifier  
+ TritonBackendEnsemble  
+ TritonOnnxYolo  
+ **apps**  
+ **deepstream_python_apps**  
+ gst-plugins  
+ includes  
+ libs  
+ objectDetector_Yolo  
+ tools  
+ tracker_ReID

  + deepstream_python_apps: Run example deepstream with python
    `3rdparty  FAQ.md  HOWTO.md  LICENSE  README.md  THIRD_PARTY_LICENSE  apps  bindings  docs  notebooks  tests`
    + 3rdparty: `gstreamer  pybind11` **Initialization of submodules and Installing Gst-python in HERE**
    + bindings: **Compiling the bindings in HERE**
    + apps: TEST first example in HERE
      + `README                               deepstream-imagedata-multistream            deepstream-opticalflow       deepstream-segmentation    deepstream-test1-usbcam  runtime_source_add_delete
        common                               deepstream-imagedata-multistream-cupy       deepstream-preprocess-test   deepstream-ssd-parser      deepstream-test2
        deepstream-custom-binding-test       deepstream-imagedata-multistream-redaction  deepstream-rtsp-in-rtsp-out  deepstream-test1           deepstream-test3
        deepstream-demux-multi-in-multi-out  deepstream-nvdsanalytics                    deepstream-segmask           deepstream-test1-rtsp-out  deepstream-test4`
  + apps: Run example deepstream with C/C++
    `apps-common  audio_apps  sample_apps`
    + /opt/nvidia/deepstream/deepstream/sources/apps/sample_apps/deepstream-test3
    + `Makefile  README  deepstream_test3_app.c  dstest3_config.yml  dstest3_pgie_config.txt  dstest3_pgie_config.yml  dstest3_pgie_nvinferserver_config.txt`
    