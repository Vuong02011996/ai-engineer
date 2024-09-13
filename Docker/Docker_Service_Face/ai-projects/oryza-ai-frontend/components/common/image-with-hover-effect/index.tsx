import { Stack } from '@mui/material';

interface IImageWithHoverEffect {
    url: string;
}

export const ImageWithHoverEffect = (props: IImageWithHoverEffect) => {
    const { url } = props;
    return (
        <Stack
            sx={{
                height: '100%',
                backgroundColor: '#55595d',
                // display: 'block',
                '&:hover  #image-hover-effect ': {
                    opacity: '1 !important',
                    visibility: 'visible !important',
                },

                '& #image-hover-base ': {
                    height: {
                        xs: '80px',
                        md: '100px',
                    },
                    width: {
                        xs: '150px',
                        md: '200px',
                    },

                    '&  img ': {
                        height: {
                            xs: '80px',
                            md: '100px',
                        },
                        width: {
                            xs: '150px',
                            md: '200px',
                        },
                    },
                },
            }}
        >
            <picture
                id="image-hover-base"
                style={{
                    display: 'flex',
                    flexDirection: 'column',
                    boxSizing: 'border-box',
                    justifyContent: 'center',
                    alignItems: 'center',
                }}
            >
                <img
                    src={url}
                    style={{
                        objectFit: 'contain',
                    }}
                    alt="big img"
                />
            </picture>

            {/* <div
                style={{
                    width: '300px',
                    height: '200px',
                    backgroundColor: 'gray',
                    position: 'fixed',
                    bottom: 10,
                    left: 10,
                    zIndex: 500,
                    display: 'none',
                    backgroundImage: `url(${url})`,
                    backgroundSize: 'cover',
                    backgroundPosition: 'center',
                }}
            >
                
            </div> */}

            <picture
                id="image-hover-effect"
                style={{
                    backgroundColor: 'gray',
                    position: 'fixed',
                    bottom: 10,
                    left: 10,
                    zIndex: 5000,
                    opacity: '0 !important',
                    visibility: 'hidden',
                    justifyContent: 'center',
                    alignItems: 'center',
                    border: '1px solid black',
                    boxShadow: 'rgba(0, 0, 0, 0.24) 0px 3px 8px;',
                }}
            >
                <img
                    src={url}
                    alt="photo"
                    style={{
                        maxHeight: '300px',
                        maxWidth: '700px',
                        minWidth: '600px',
                        objectFit: 'contain',
                    }}
                />
            </picture>
        </Stack>
    );
};
