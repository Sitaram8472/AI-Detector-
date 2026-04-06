from src.pipeline.predict_pipeline import predict

def test():
    sample = "Artificial intelligence is transforming industries."
    result = predict(sample)
    print(result)

if __name__ == "__main__":
    test()