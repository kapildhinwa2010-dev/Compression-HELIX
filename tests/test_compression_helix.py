import pytest
import torch
from compression_helix import CompressionHELIX, create_compression_helix

class TestCompressionHELIX:
    def test_init(self):
        m = CompressionHELIX(dim=256, hidden_dim=512)
        assert m.dim == 256
    
    def test_forward(self):
        m = CompressionHELIX(dim=256)
        x = torch.randn(32, 256)
        assert m(x).shape == (32, 256)
    
    def test_factory(self):
        m = create_compression_helix()
        assert isinstance(m, CompressionHELIX)

if __name__ == '__main__':
    pytest.main([__file__, '-v'])
